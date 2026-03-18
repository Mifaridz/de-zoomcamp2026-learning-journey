import pandas as pd	# type: ignore
import json
from time import time
from kafka import KafkaProducer	# pyright: ignore[reportMissingImports]

# Inisialisasi Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 1. Gunakan URL Green Taxi Oktober 2025 sesuai instruksi homework
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"

# 2. Baca kolom yang diminta (PENTING: Jangan gunakan .head())
columns = [
    'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 
    'DOLocationID', 'passenger_count', 'trip_distance', 
    'tip_amount', 'total_amount'
]

print("Sedang mengunduh dan membaca dataset...")
df = pd.read_parquet(url, columns=columns)

# 3. Konversi datetime ke string agar JSON serializable
df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].astype(str)
df['lpep_dropoff_datetime'] = df['lpep_dropoff_datetime'].astype(str)

# --- MULAI PENGUKURAN WAKTU ---
print(f"Memulai pengiriman {len(df)} baris data...")
t0 = time()

topic_name = 'green-trips'

for row in df.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in columns}
    producer.send(topic_name, value=row_dict)

# Flush sangat krusial agar semua data terkirim sebelum timer berhenti
producer.flush()

t1 = time()
# --- SELESAI PENGUKURAN WAKTU ---

print(f'took {(t1 - t0):.2f} seconds')