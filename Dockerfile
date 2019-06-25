FROM python:3.7-alpine

COPY requirements.txt .

RUN pip install -r requirements.txt && \
  addgroup -S kopf && adduser -S kopf -G kopf

WORKDIR /usr/src/app

COPY --chown=kopf:kopf handlers.py .

USER kopf

CMD ["/usr/local/bin/kopf", "run", "--standalone", "handlers.py"]
