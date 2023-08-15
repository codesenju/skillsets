const process = require('process');
const opentelemetry = require("@opentelemetry/sdk-node");
const { Resource } = require("@opentelemetry/resources");
const { SemanticResourceAttributes } = require("@opentelemetry/semantic-conventions");
const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { AWSXRayPropagator } = require("@opentelemetry/propagator-aws-xray");
const { AWSXRayIdGenerator } = require("@opentelemetry/id-generator-aws-xray");
const { HttpInstrumentation } = require("@opentelemetry/instrumentation-http");
const { AwsInstrumentation } = require("@opentelemetry/instrumentation-aws-sdk");
const { getNodeAutoInstrumentations } = require("@opentelemetry/auto-instrumentations-node");
const { PeriodicExportingMetricReader, ConsoleMetricExporter } = require('@opentelemetry/sdk-metrics');
const { ConsoleSpanExporter } = require('@opentelemetry/sdk-trace-node');
const { diag, DiagConsoleLogger, DiagLogLevel } = require('@opentelemetry/api');
const { detectResources } = require('@opentelemetry/resources');
const { awsEksDetector, awsEc2Detector , awsEcsDetector} = require('@opentelemetry/resource-detector-aws');
const { containerDetector } = require('@opentelemetry/resource-detector-container');

const _resource = Resource.default().merge(new Resource({
  [SemanticResourceAttributes.SERVICE_NAME]: "nextjs-ui",
}));

const otel_url = process.env.OTEL_ENDPOINT_GRPC;

const _traceExporter = new OTLPTraceExporter({
  url: otel_url,
});

const _spanProcessor = new BatchSpanProcessor(_traceExporter);

const _tracerConfig = {
  idGenerator: new AWSXRayIdGenerator()
}

// For troubleshooting, set the log level to DiagLogLevel.DEBUG
diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.DEBUG);


// Using the AWS Resource Detectors | AwsEksDetector, awsEcsDetector
async function start() {
  const resource = await detectResources({
    detectors: [awsEksDetector, awsEcsDetector, containerDetector],
  });

  const sdk = new opentelemetry.NodeSDK({
    textMapPropagator: new AWSXRayPropagator(),
    instrumentations: [
      new HttpInstrumentation(),
      new AwsInstrumentation({
        suppressInternalInstrumentation: true
      }),
    ],
    resource: _resource.merge(resource),
    spanProcessor: _spanProcessor,
    traceExporter: _traceExporter,
    // instrumentations: [getNodeAutoInstrumentations()],
    /*metricReader: new PeriodicExportingMetricReader({
      exporter: new ConsoleMetricExporter()
    }),*/
  });
  sdk.configureTracerProvider(_tracerConfig, _spanProcessor);
  // this enables the API to record telemetry
  sdk.start();
  // gracefully shut down the SDK on process exit
  process.on('SIGTERM', () => {
    sdk.shutdown()
      .then(() => console.log('Tracing and Metrics terminated'))
      .catch((error) => console.log('Error terminating tracing and metrics', error))
      .finally(() => process.exit(0));
  });
}

start();
