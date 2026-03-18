import os
from pyflink.table import EnvironmentSettings, TableEnvironment	# pyright: ignore[reportMissingImports]

def run_session_job():
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = TableEnvironment.create(settings)
    t_env.get_config().set("parallelism.default", "1")

    # Source DDL (Green Trips)
    t_env.execute_sql("""
        CREATE TABLE green_trips (
            lpep_pickup_datetime STRING,
            PULocationID INT,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'homework-q5-group',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """)

    # Sink DDL (Postgres)
    t_env.execute_sql("""
        CREATE TABLE sink_postgres (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            PULocationID INT,
            num_trips BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'processed_sessions_q5',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    # Query Session Window (Gap 5 Menit)
    t_env.execute_sql("""
        INSERT INTO sink_postgres
        SELECT 
            SESSION_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
            SESSION_END(event_timestamp, INTERVAL '5' MINUTE) AS window_end,
            PULocationID,
            COUNT(*) as num_trips
        FROM green_trips
        GROUP BY 
            SESSION(event_timestamp, INTERVAL '5' MINUTE),
            PULocationID
    """)

if __name__ == '__main__':
    run_session_job()