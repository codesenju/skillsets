const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { LogLevel } = require('@opentelemetry/core');
const { NodeTracerProvider } = require('@opentelemetry/node');
const { SimpleSpanProcessor } = require('@opentelemetry/tracing');
const { OTLPHttpSpanExporter } = require('@opentelemetry/exporter-otlp-http');

const serviceName = 'skillsets-ui';
const collectorEndpoint = 'http://otel-collector:4317';

const provider = new NodeTracerProvider({
  logLevel: LogLevel.ERROR,
});

const exporter = new OTLPHttpSpanExporter({
  serviceName,
  endpoint: collectorEndpoint,
});

provider.addSpanProcessor(new SimpleSpanProcessor(exporter));

provider.register();

registerInstrumentations({
  instrumentations: [getNodeAutoInstrumentations()],
});

console.log('Tracing initialized');
