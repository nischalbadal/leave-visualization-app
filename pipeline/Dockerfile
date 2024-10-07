FROM python:3.9-slim

WORKDIR /pipeline/src

COPY ../requirements.txt /pipeline/src/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY files/ /pipeline/files/
COPY src/ /pipeline/src/

VOLUME /pipeline/qc_reports

ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_NAME

ENTRYPOINT ["python"]
