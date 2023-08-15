FROM python:3.11.2-bullseye

WORKDIR /app

ENV REDIS_PORT=6379
ENV REDIS_HOST=localhost
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

COPY ./requirements.txt .
COPY ./app.py  .

RUN apt-get update -y && \
    apt-get install -y bind9-utils curl dnsutils ncat stress && \
    pip install --no-cache-dir -r requirements.txt

RUN pip install opentelemetry-distro && \
    pip install opentelemetry-exporter-otlp && \
    pip install opentelemetry-exporter-otlp-proto-http && \
## X-Ray Integration ##
# You also need the opentelemetry-propagator-aws-xray package 
# to obtain the AwsXRayPropagator class used to propagate the 
# trace context across AWS services.
# https://aws-otel.github.io/docs/getting-started/python-sdk/trace-auto-instr
    pip install opentelemetry-sdk-extension-aws && \
    pip install opentelemetry-propagator-aws-xray && \
    opentelemetry-bootstrap -a install

# CMD opentelemetry-instrument \
#    --traces_exporter otlp \
#    --metrics_exporter otlp \ 
#    --service_name skillsets \
#   flask run
CMD uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app
# CMD flask run