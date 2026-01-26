import os
import pandas as pd
from sqlalchemy import create_engine
from time import time

# 1. Configure PostgreSQL Database Connection
# User: postgres, Pass: postgres, Host: localhost, Port: 5433, DB: ny_taxi
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

# 2. Download & Ingest Data Zona (CSV)
print("Downloading Zones data...")
os.system("wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv -O zones.csv")

df_zones = pd.read_csv('zones.csv')
df_zones.to_sql(name='zones', con=engine, if_exists='replace')
print("Tabel 'zones' selesai.")

# 3. Download & Ingest Data Trip (Parquet)
print("Downloading Trip data...")
# Note: Parquet files are more efficient than CSV for large datasets
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
os.system(f"wget {url} -O green_tripdata_2025-11.parquet")

print("Reading parquet...")
df = pd.read_parquet('green_tripdata_2025-11.parquet')

print("Ingesting trip data to Postgres...")
# Note: Using automatic chunking from pandas/sqlalchemy for large datasets
df.to_sql(name='green_taxi_trips', con=engine, if_exists='replace', chunksize=100000)
print("Selesai! Data siap di-query.")