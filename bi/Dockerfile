ARG FROM_IMAGE=python:3.10.6-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=bi

ENV PROJECT_DIR=opt
WORKDIR /${PROJECT_DIR}
COPY ${LOCAL_DIR}/requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY ${LOCAL_DIR}/src/ /${PROJECT_DIR}/src/

ENV PYTHONPATH=/${PROJECT_DIR}

CMD [ "streamlit", "run", "src/main.py", "--server.address=0.0.0.0" ]
