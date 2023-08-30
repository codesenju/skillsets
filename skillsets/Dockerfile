
# FROM python:3.11.2-bullseye
FROM  python:slim-bookworm
WORKDIR /app
ENV REDIS_PORT=6379
ENV REDIS_HOST=localhost
COPY ./requirements.txt .
COPY ./app.py  .

# # Run bandit/safety for source code security checks and package checks
# RUN pip install bandit==1.7.5 safety==2.3.5 && \
#     bandit app.py && \
#     safety check -r requirements.txt

RUN apt-get update --no-install-recommends -y && \
    apt-get install --no-install-recommends -y bind9-utils curl dnsutils ncat stress gcc python3-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    # Automatically detect and install OpenTelemetry python packages. 
    opentelemetry-bootstrap -a install

RUN chown nobody . -R
USER nobody
EXPOSE 5000
# CMD opentelemetry-instrument uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app
ENTRYPOINT opentelemetry-instrument gunicorn -w 4 -b 0.0.0.0:5000 app:app
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/healthz || exit 1