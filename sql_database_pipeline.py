from typing import Any, Iterator

import dlt
from dlt.sources.credentials import ConnectionStringCredentials
from sql_database import Table, sql_database, sql_table


def load_select_tables_from_database() -> None:
    """Use the sql_database source to reflect an entire database schema and load select tables from it.
    """
    # Create a pipeline
    pipeline = dlt.pipeline(
        pipeline_name="Azure_Events_Type_2", destination='snowflake', dataset_name="Event_Type"
    )

    # Credentials for the sample database.
    # Note: It is recommended to configure credentials in `.dlt/secrets.toml` under `sources.sql_database.credentials`
    credentials = dlt.secrets["sources.sql_database.credentials"]["connection_string"]

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



if __name__ == "__main__":
    # Load selected tables with different settings
    load_select_tables_from_database()

