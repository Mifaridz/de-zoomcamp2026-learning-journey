import os
from pyflink.table import EnvironmentSettings, TableEnvironment	# pyright: ignore[reportMissingImports]

def run_aggregation_job():
    # 1. Inisialisasi Environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = TableEnvironment.create(settings)
    
    # PENTING untuk homework ini: Parallelism harus 1
    t_env.get_config().set("parallelism.default", "1")

    # 2. Source DDL: Membaca dari Redpanda (green-trips)
    # Gunakan pemrosesan timestamp string sesuai instruksi soal
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
            'properties.group.id' = 'homework-q4-group',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """)

    # 3. Sink DDL: Menulis ke PostgreSQL
    t_env.execute_sql("""
        CREATE TABLE sink_postgres (
            window_start TIMESTAMP(3),
            PULocationID INT,
            num_trips BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'processed_trips_q4',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """)

    # 4. Windowing Query: Tumbling Window 5 Menit
    t_env.execute_sql("""
        INSERT INTO sink_postgres
        SELECT 
            TUMBLE_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
            PULocationID,
            COUNT(*) as num_trips
        FROM green_trips
        GROUP BY 
            TUMBLE(event_timestamp, INTERVAL '5' MINUTE),
            PULocationID
    """)

if __name__ == '__main__':
    run_aggregation_job()