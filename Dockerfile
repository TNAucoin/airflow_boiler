FROM apache/airflow:2.8.2
USER root

# Install additional root level packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential

# Run remaining commands as the airflow runtime user \
USER airflow
COPY ./config/airflow.cfg /opt/airflow/airflow.cfg
COPY ./plugins /opt/airflow/plugins
COPY ./dags /opt/airflow/dags

# Install pip packages into the container that DAG code needs
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt