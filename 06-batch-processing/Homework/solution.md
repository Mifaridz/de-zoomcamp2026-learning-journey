# Module 6 Homework: Batch Processing with Spark

## Overview

This repository contains my solutions for **Module 6** of the Data Engineering Zoomcamp.

In this module, I practiced using **Apache Spark** for distributed batch data processing.

The exercises involve installing Spark, working with PySpark, processing NYC Taxi datasets, and performing analytical queries using Spark DataFrames.

---

## Technologies Used

- **Apache Spark** – Distributed data processing engine
- **PySpark** – Python API for Spark
- **Python**
- **Parquet** – Columnar storage format
- **NYC Taxi Dataset**

---

## Homework Solutions

### Question 1: Install Spark and PySpark

**Objective:** Install Apache Spark, run PySpark, create a Spark session, and check the Spark version.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/06-batch-processing/Homework/images/question-1.png?raw=true)

**Answer:** `Spark Version: 4.1.1`

**Steps:**

1. I installed Apache Spark following the official installation guide.
2. I verified that Java and Python were correctly installed on my system.
3. I launched PySpark using the terminal and created a local Spark session.
4. Inside my Jupyter Notebook / PySpark shell, I executed the version command.

```python
import pyspark
from pyspark.sql import SparkSession

# Create a local spark session
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Module6_Homework") \
    .getOrCreate()

# Check the output
spark.version

```

**Explanation:** The `spark.version` command returns the version of Apache Spark that is currently running in the active Spark session.

---

### Question 2: Yellow November 2025

**Objective:** Load the Yellow Taxi dataset for November 2025, repartition it into 4 partitions, and save it as Parquet files. Find the average size of the created Parquet files.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/06-batch-processing/Homework/images/question-2.png?raw=true)

**Answer:** `25MB`

**Steps:**

1. I downloaded the dataset using `wget`.
2. I loaded the dataset into a Spark DataFrame.
3. I repartitioned the DataFrame into 4 partitions.
4. I saved the repartitioned data as Parquet files.
5. I checked the size of each `.parquet` file created using terminal commands.

```bash
# Download the dataset
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet

```

```python
# Read the data into a DataFrame
df = spark.read.parquet("yellow_tripdata_2025-11.parquet")

# Repartition and save
df = df.repartition(4)
df.write.mode("overwrite").parquet("yellow_tripdata_2025-11-repartitioned")

```

```bash
# Check the file sizes in the terminal
ls -lh yellow_tripdata_2025-11-repartitioned/

```

---

### Question 3: Count records

**Objective:** Determine how many taxi trips started on November 15th.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/06-batch-processing/Homework/images/question-3.png?raw=true)

**Answer:** `162604`

**Steps:**

1. I imported the necessary SQL functions from PySpark.
2. I filtered the DataFrame to strictly include rows where the pickup datetime matched "2025-11-15".
3. I executed the `count()` action to get the total records.

```python
from pyspark.sql.functions import col, to_date

# Filter and count
trips_on_15th = df.filter(to_date(col("tpep_pickup_datetime")) == "2025-11-15").count()
print(trips_on_15th)

```

**Explanation:** This query filters the dataset by converting the timestamp to a standard date format, ensuring we only capture trips that initiated exactly on November 15th.

---

### Question 4: Longest trip

**Objective:** Find the longest trip duration in the dataset in hours.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/06-batch-processing/Homework/images/question-4.png?raw=true)

**Answer:** `90.6`

**Steps:**

1. I calculated the duration of each trip by subtracting the pickup timestamp from the dropoff timestamp.
2. To perform accurate math, I cast both columns to `long` (seconds) and divided by 3600 to convert the difference into hours.
3. I aggregated the data to find the maximum `trip_duration`.

```python
from pyspark.sql.functions import col

# Calculate duration and find max
longest_trip = (df.withColumn(
    "trip_duration_hours",
    (col("tpep_dropoff_datetime").cast("long") -
     col("tpep_pickup_datetime").cast("long")) / 3600
).agg({"trip_duration_hours": "max"}))

longest_trip.show()

```

---

### Question 5: User Interface

**Objective:** Identify the local port where the Spark Web UI runs.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/06-batch-processing/Homework/images/question-5.png?raw=true)

**Answer:** `4040`

**Explanation:** Spark automatically starts a monitoring interface (Web UI) for each application context. By default, it binds to port `4040` on the local machine (accessible via `localhost:4040`). If port `4040` is taken, it will sequentially try `4041`, `4042`, and so on.

---

### Question 6: Least frequent pickup location zone

**Objective:** Load the zone lookup data and find the name of the LEAST frequent pickup location Zone.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/06-batch-processing/Homework/images/question-6.png?raw=true)

**Answer:** `Governor's Island/Ellis Island/Liberty Island`

**Steps:**

1. I downloaded the `taxi_zone_lookup.csv` file using `wget`.
2. I loaded the CSV into a DataFrame and registered it as a temporary view named `zones`.
3. I registered my main Yellow Taxi DataFrame as a temporary view named `trips`.
4. I executed a Spark SQL query to join the tables, group by the zone name, count the occurrences, and sort in ascending order to find the least frequent pickup zone.

```bash
# Download the lookup data
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv

```

```python
# Read lookup data and create temp views
zones = spark.read.option("header", True).csv("taxi_zone_lookup.csv")

zones.createOrReplaceTempView("zones")
df.createOrReplaceTempView("trips")

# Execute Spark SQL Query
spark.sql("""
SELECT z.Zone, COUNT(*) as trips_count
FROM trips t
JOIN zones z
ON t.PULocationID = z.LocationID
GROUP BY z.Zone
ORDER BY trips_count ASC
LIMIT 1
""").show()

```

---

## Key Takeaways

- I practiced using Apache Spark for distributed batch data processing.
- I learned how Spark partitions data to improve parallel processing.
- I gained experience writing analytical queries using Spark DataFrames and Spark SQL.
- I also explored the Spark Web UI for monitoring jobs and stages.

---
