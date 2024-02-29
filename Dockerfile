FROM apache/airflow:2.8.2
USER root

# Install additional root level packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    unzip \
    odbcinst1debian2 \
    odbcinst \
    libodbc1 \
    unixodbc

# Set the output directory for the downloaded file
WORKDIR /usr/local/airflow

COPY ./instantclient_19_22 ./instantclient_19_22

# Set environment variables
ENV LD_LIBRARY_PATH="/usr/local/airflow/instantclient_19_22"
ENV DPI_DEBUG_LEVEL="64"

# Clean up apt cache and packages
RUN apt-get clean && rm -rf /var/lib/apt/lists/*


# Run remaining commands as the airflow runtime user \
USER airflow
COPY ./config/airflow.cfg /opt/airflow/airflow.cfg
COPY ./plugins /opt/airflow/plugins
COPY ./dags /opt/airflow/dags

# Install pip packages into the container that DAG code needs
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt