# Airflow-boiler

This is a boilerplate for Airflow. It is a simple project that can be used as a starting point for new Airflow projects.

## Overview
To streamline the deployment and management of our Airflow stack both locally and in production, we adopt a Docker-centric approach. We utilize Docker containers for the runtime environment, coupled with Docker Compose to define and orchestrate the entire stack. This configuration provides a distinct separation between the Airflow dependencies, such as pip and apt packages, and our Airflow application code. The latter includes DAGs, operators, and plugin code, all of which are authored in Python.

## Repository Structure
The repository is organized as follows:

```
airflow-boiler/
├── dags/
│   ├── project_1/
│   └── example_dag.py
├── plugins/
│   ├── operators/
│   └── some_operator_plugin.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```
This gives the ability to split your DAGs out per project and share common operators between DAGs, be they coupled to a single project or a decoupled common utility

> All DAGs are presented in a single table, but an effective way to delineate ownership between the DAGs is to [configure owners and tag’s for each DAG](https://github.com/TNAucoin/airflow_boiler/blob/604e19972eb8c5da0a7b8aed87e3f7444c25d966/dags/test_dag/test_dag.py#L15). It may also be effective to document this information in the DAG docs strings. [More details are in the following article](https://levelup.gitconnected.com/airflow-dag-and-task-markdown-docs-2c00c72152b4).

The plugins folder gets included in the Python sys path when it's mounted into Airflow. Consequently, anything within this folder can be imported just like a regular Python module in your DAG code. This approach allows you to apply packaging patterns to organize your Python utilities, operators, hooks, etc., according to your requirements, whether it's dividing them into common, project-specific, or client-specific folders.

## Dockerfile

The [provided Dockerfile](https://github.com/TNAucoin/airflow_boiler/blob/604e19972eb8c5da0a7b8aed87e3f7444c25d966/Dockerfile#L1) presents a fundamental configuration extending the official Airflow image to install necessary dependencies for our DAG code. For detailed information on extending the base Airflow Docker image to meet your project requirements, you can consult the [documentation provided by Airflow](https://airflow.apache.org/docs/docker-stack/build.html#extending-the-image).

## Docker Compose

```bash
# Build the local extended Airflow container using the local Dockerfile
docker-compose build
# Run all of the containers used in the stack
# The -d flag runs the containers in the background
# otherwise your terminal will be taken over by the logs of the running containers
docker-compose up -d
# Take down the airflow stack gracefully
docker-compose down
```
once the stack is running, you can access the Airflow UI at [http://localhost:8080](http://localhost:8080)

> Note the [configuration of mounts](https://github.com/TNAucoin/airflow_boiler/blob/604e19972eb8c5da0a7b8aed87e3f7444c25d966/docker-compose.yml#L21) for our local DAGs and Python plugin files in the Docker Compose volume block. This setup enables rapid development by immediately updating running DAGs with local file changes. This eliminates the need to sync files and update the entire Airflow stack with each code change, allowing for quick identification of any broken logic in DAGs or operator code.