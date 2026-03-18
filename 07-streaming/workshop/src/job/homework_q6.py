import os
from pyflink.table import EnvironmentSettings, TableEnvironment	# pyright: ignore[reportMissingImports]

def run_tip_aggregation_job():
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = TableEnvironment.create(settings)
    t_env.get_config().set("parallelism.default", "1")

    # Source DDL (Green Trips)
    # Kita butuh lpep_pickup_datetime untuk waktu dan tip_amount untuk dihitung
    t_env.execute_sql("""
        CREATE TABLE green_trips (
            lpep_pickup_datetime STRING,
            tip_amount FLOAT,
            event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'properties.group.id' = 'homework-q6-group',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """)

    # Sink DDL (Postgres)
    t_env.execute_sql("""
        CREATE TABLE sink_postgres (
            window_start TIMESTAMP(3),
            tip_amount_sum FLOAT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'processed_tips_q6',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    # Query Tumbling Window 1 Jam
    t_env.execute_sql("""
        INSERT INTO sink_postgres
        SELECT 
            TUMBLE_START(event_timestamp, INTERVAL '1' HOUR) AS window_start,
            SUM(tip_amount) as tip_amount_sum
        FROM green_trips
        GROUP BY 
            TUMBLE(event_timestamp, INTERVAL '1' HOUR)
    """)

if __name__ == '__main__':
    run_tip_aggregation_job()