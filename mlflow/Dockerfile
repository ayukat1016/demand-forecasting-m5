ARG FROM_IMAGE=python:3.10.6-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=mlflow

ENV PROJECT_DIR opt
WORKDIR /${PROJECT_DIR}
COPY ${LOCAL_DIR}/requirements.txt /${PROJECT_DIR}/
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "mlflow", "server", "--backend-store-uri", "/opt/outputs", "--default-artifact-root", "/opt/outputs", "--host", "0.0.0.0" ]
