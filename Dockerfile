FROM python:3.7-alpine

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY --chown=1001:1001 handlers.py .

USER 1001

CMD ["/usr/local/bin/kopf", "run", "--standalone", "handlers.py"]
