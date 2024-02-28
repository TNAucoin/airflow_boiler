from datetime import timedelta

import airflow
import dlt
from airflow.decorators import dag
#from airflow.operators.python import PythonOperator
from dlt.common import pendulum
from dlt.helpers.airflow_helper import PipelineTasksGroup
from dlt_dags.sql_database import Table, sql_database, sql_table

#from sql_database_pipeline import load_select_tables_from_database

default_task_args = {
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'execution_timeout': timedelta(seconds=5),
}

def load_select_tables_from_database() -> None:
    """Use the sql_database source to reflect an entire database schema and load select tables from it.
    """
    # Create a pipeline
    pipeline = dlt.pipeline(
        pipeline_name="Azure_Events_Type_2", destination='snowflake', dataset_name="Event_Type"
    )

    # Credentials for the sample database.
    # Note: It is recommended to configure credentials in `.dlt/secrets.toml` under `sources.sql_database.credentials`
    credentials = 'mssql+pyodbc://FiveTranExtract:n8"n+!R3d!8T*;+@qevqyjnb6y.database.windows.net:1433/EventSystemDB?driver=ODBC+Driver+17+for+SQL+Server'

    # Configure the source to load a few select tables incrementally
    source_1 = sql_database(credentials).with_resources("EventType")
    # Add incremental config to the resources. "updated" is a timestamp column in these tables that gets used as a cursor
    source_1.EventType.apply_hints(incremental=dlt.sources.incremental("EventTypeId"))

    # Run the pipeline. The merge write disposition merges existing rows in the destination by primary key
    info = pipeline.run(source_1, write_disposition="replace")
    print(info)

    # Load some other tables with replace write disposition. This overwrites the existing tables in destination
    source_2 = sql_database(credentials).with_resources("EventSource")

    info = pipeline.run(source_2, write_disposition="replace")
    print(info)


@dag(
    schedule_interval='@daily',
    start_date=pendulum.datetime(2024, 2, 27),
    catchup=False,
    max_active_runs=1,
    default_args=default_task_args
)
def load_data():
    # set `use_data_folder` to True to store temporary data on the `data` bucket. Use only when it does not fit on the local storage
    tasks = PipelineTasksGroup("pipeline_decomposed", fail_task_if_any_job_failed=True, use_data_folder=False, wipe_local_data=True)

    credentials = credentials = dlt.secrets["sources.sql_database.credentials"]["connection_string"]
    # import your source from pipeline script
    #from dlt_dags.sql_database_pipeline import load_select_tables_from_database

    # modify the pipeline parameters 
    pipeline = dlt.pipeline(pipeline_name='Azure_Event_Type_2',
                     dataset_name='EventType',
                     destination='snowflake',
                     full_refresh=False # must be false if we decompose
                     )
    # create the source, the "serialize" decompose option will converts dlt resources into Airflow tasks. use "none" to disable it
    tasks.add_run(pipeline, load_select_tables_from_database(), decompose="serialize", trigger_rule="all_done", retries=0, provide_context=True)


load_data()