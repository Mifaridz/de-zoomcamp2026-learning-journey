import json
from kafka import KafkaConsumer	# pyright: ignore[reportMissingImports]

# Inisialisasi Consumer
consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest', 
    enable_auto_commit=False, # Set False dulu agar bisa kita tes berulang-ulang
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    consumer_timeout_ms=10000 # Naikkan ke 10 detik untuk jaga-jaga
)

count_distance_gt_5 = 0
total_processed = 0

print("Mencoba menghubungkan ke Redpanda...")

# Cek apakah ada assignment partisi
print(f"Topic yang dipantau: {consumer.topics()}")

try:
    for message in consumer:
        total_processed += 1
        trip_data = message.value
        
        distance = trip_data.get('trip_distance', 0)
        if distance > 5.0:
            count_distance_gt_5 += 1
            
        if total_processed % 10000 == 0:
            print(f"Sedang memproses... total sementara: {total_processed}")

except Exception as e:
    print(f"Error: {e}")

if total_processed == 0:
    print("⚠️ PERINGATAN: Tidak ada pesan yang terbaca sama sekali!")
    print("Pastikan Producer sudah dijalankan sebelumnya dan Topic 'green-trips' tidak kosong.")
else:
    print("-" * 30)
    print(f"Total pesan yang diperiksa: {total_processed}")
    print(f"Jawaban Question 3: {count_distance_gt_5}")
    print("-" * 30)