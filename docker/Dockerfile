FROM puckel/docker-airflow:latest
USER root

RUN mkdir -p /usr/share/man/man1 && \
    apt-get update -y && \
    apt-get install -y \
                    procps \
                    libsnappy-dev \

                    unzip \
                    && \
    apt-get autoremove -y

COPY docker/entrypoint.sh /entrypoint.sh
RUN rm $AIRFLOW_HOME/airflow.cfg
# install python requirements during the build time
# results in faster builds for development
COPY requirements-airflow.txt requirements.txt
RUN pip3 install -r requirements.txt

USER airflow
