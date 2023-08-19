FROM python:3.11.2-bullseye

WORKDIR /app

ENV REDIS_PORT=6379
ENV REDIS_HOST=localhost

COPY ./requirements.txt .
COPY ./app.py  .

RUN apt-get update -y && \
    apt-get install --no-install-recommends -y bind9-utils curl dnsutils ncat stress && \
    pip install --no-cache-dir -r requirements.txt && \
    # Automatically detect and install OpenTelemetry python packages. 
    opentelemetry-bootstrap -a install

RUN chown nobody:nobody . -R
USER nobody
EXPOSE 5000
CMD opentelemetry-instrument uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/healthz || exit 1