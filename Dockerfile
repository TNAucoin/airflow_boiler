FROM apache/airflow:2.8.2
USER root

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    unzip \
    alien \
    wget \
    gnupg2 \
    libaio1

# Install ODBC driver for SQL Server
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    wget -qO- https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install Oracle Instant Client
RUN wget https://download.oracle.com/otn_software/linux/instantclient/214000/oracle-instantclient-basiclite-21.4.0.0.0-1.x86_64.rpm && \
    alien -i oracle-instantclient-basiclite-21.4.0.0.0-1.x86_64.rpm && \
    echo "/usr/lib/oracle/21/client64/lib" > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig && \
    rm oracle-instantclient-basiclite-21.4.0.0.0-1.x86_64.rpm

# Set environment variables
ENV LD_LIBRARY_PATH /usr/lib/oracle/21/client64/lib
# Clean up apt cache and packages
RUN apt-get clean && rm -rf /var/lib/apt/lists/*


# Run remaining commands as the airflow runtime user \
USER airflow
COPY ./config/airflow.cfg /opt/airflow/airflow.cfg
COPY ./plugins /opt/airflow/plugins
COPY ./dags /data/airflow/dags
COPY ./.dlt /home/airflow/.local/bin/.dlt

# Install pip packages into the container that DAG code needs
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
