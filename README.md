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

> All DAGs are presented in a single table, but an effective way to delineate ownership between the DAGs is to [configure owners and tag’s for each DAG](https://github.com/TNAucoin/airflow_boiler/blob/9ef529f58278e0f8f7226e76a5f0049bf299f5f7/dags/test_dag/test_dag.py#L16). It may also be effective to document this information in the DAG docs strings. [More details are in the following article](https://levelup.gitconnected.com/airflow-dag-and-task-markdown-docs-2c00c72152b4).

The plugins folder gets included in the Python sys path when it's mounted into Airflow. Consequently, anything within this folder can be imported just like a regular Python module in your DAG code. This approach allows you to apply packaging patterns to organize your Python utilities, operators, hooks, etc., according to your requirements, whether it's dividing them into common, project-specific, or client-specific folders.
