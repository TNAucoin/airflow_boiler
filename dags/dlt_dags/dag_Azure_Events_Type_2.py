from datetime import timedelta

import airflow
import dlt
from airflow.decorators import dag
from dlt.common import pendulum
from dlt.helpers.airflow_helper import PipelineTasksGroup
from dlt_dags.sql_database import Table, sql_database, sql_table
from datetime import timedelta
from functools import lru_cache
#from sql_database_pipeline import load_select_tables_from_database

default_task_args = {
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'execution_timeout': timedelta(seconds=5),
}

@lru_cache(maxsize=1)
def get_azure_db_connection_string():
    return dlt.secrets["sources.sql_database.credentials"]["connection_string"]

@dag(
    schedule_interval='@daily',
    start_date=pendulum.datetime(2024, 2, 27),
    catchup=False,
    max_active_runs=1,
    default_args= {
        'execution_timeout': timedelta(minutes=10)
    },

)

def load_azure_events_data():
    # set `use_data_folder` to True to store temporary data on the `data` bucket. Use only when it does not fit on the local storage
    tasks = PipelineTasksGroup("Azure_Event", fail_task_if_any_job_failed=True, use_data_folder=False, wipe_local_data=True)

    azure_credentials = get_azure_db_connection_string()
    #snow_creds = dlt.secrets["destination.snowflake.credentials.database"]
    # import your source from pipeline script
    #from dlt_dags.sql_database_pipeline import load_select_tables_from_database

    # modify the pipeline parameters 
    pipeline = dlt.pipeline(pipeline_name='Azure_Event_Type_2',
                     dataset_name='EventType',
                     destination='snowflake',
                     credentials= dlt.secrets["destination.snowflake.credentials"],
                     full_refresh=False # must be false if we decompose
                     )
    
    source_1 = sql_database(azure_credentials, schema='dbo').with_resources("EventType")
                         
    # create the source, the "serialize" decompose option will converts dlt resources into Airflow tasks. use "none" to disable it
    tasks.add_run(pipeline, source_1, decompose="none", trigger_rule="all_done", retries=0, provide_context=True)
    
    info = pipeline.run(source_1, write_disposition="replace")
    print(info)
    
    source_2 = sql_database(azure_credentials).with_resources("EventSource")
    #source_2.EventSource.apply_hints(incremental=dlt.source.incremental("EventSource"))
    info = pipeline.run(source_2, write_disposition="replace")
    print(info)
    

load_azure_events_data()