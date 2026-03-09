from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Memulai session
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Homework_Module_6") \
    .getOrCreate()

# JAWABAN SOAL 1: Cek versi
print(f"Spark Version: {spark.version}")
