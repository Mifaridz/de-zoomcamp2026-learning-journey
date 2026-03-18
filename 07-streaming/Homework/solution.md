# Module 7 Homework: Streaming with Redpanda and PyFlink

## Overview

This project focuses on the implementation of a real-time data streaming pipeline using the **October 2025 Green Taxi Trip** dataset. The objective is to simulate a production-grade streaming environment where data is ingested, processed, and analyzed in motion rather than in batches.

Throughout this module, I practiced:

- Setting up a Kafka-compatible streaming infrastructure with **Redpanda**.
- Developing Python producers to ingest Parquet data into stream topics.
- Building stream processing jobs using **PyFlink** to perform complex aggregations.
- Implementing various windowing strategies (Tumbling and Session windows) to derive temporal insights.

---

## Technologies Used

- **Redpanda:** A modern, C++ based Kafka-compatible event streaming platform used as the message broker.
- **Apache Flink (PyFlink):** A distributed processing engine for stateful computations over data streams.
- **Docker & Docker Compose:** Containerization for managing the Redpanda broker, Flink JobManager/TaskManager, and PostgreSQL.
- **PostgreSQL:** Served as the sink database for storing processed streaming results.
- **Python:** The primary language for writing the producer, consumer, and Flink jobs, leveraging the `uv` package manager for efficient dependency handling.

---

## Streaming Architecture

The data flow follows a standard real-time architecture:

1.  **Producer:** A Python script reads Green Taxi Parquet files, transforms rows into JSON, and sends them to Redpanda.
2.  **Broker (Redpanda):** Manages the `green-trips` topic, ensuring low-latency message persistence.
3.  **Stream Processor (PyFlink):** Consumes data from the topic, applies transformations, handles event-time watermarking, and performs windowed aggregations.
4.  **Sink (Postgres):** Final aggregated results are written to relational tables for downstream visualization and querying.

---

## Homework Solutions

### Question 1: Redpanda version

**Objective:** Verify the internal version of the Redpanda broker running within the Docker container.

**Answer:** `v25.3.9`

**Steps:** 1. Access the running Redpanda container using `docker exec`. 2. Run the `rpk` (Redpanda Keeper) CLI tool to check the version.

**Code:**

```bash
docker exec -it workshop-redpanda-1 rpk version
```

---

### Question 2: Sending data to Redpanda

**Objective:** Ingest specific columns of the Green Taxi Parquet dataset into the `green-trips` topic and measure the ingestion performance.

**Answer:** `10 seconds`

**Steps:** 1. Read the `green_tripdata_2025-10.parquet` file using `pandas`. 2. Select the required 8 columns (pickups, dropoffs, locations, and amounts). 3. Initialize a Kafka Producer pointing to `localhost:9092`. 4. Iterate through rows, convert to JSON (handling datetime as strings), and send messages. 5. Use `producer.flush()` to ensure all data is sent before measuring final time.

**Code:**

```python
import pandas as pd
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

df = pd.read_parquet('green_tripdata_2025-10.parquet')
df = df[['lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID',
         'DOLocationID', 'passenger_count', 'trip_distance', 'tip_amount', 'total_amount']]

for row in df.itertuples(index=False):
    row_dict = row._asdict()
    row_dict['lpep_pickup_datetime'] = str(row_dict['lpep_pickup_datetime'])
    row_dict['lpep_dropoff_datetime'] = str(row_dict['lpep_dropoff_datetime'])
    producer.send('green-trips', json.dumps(row_dict).encode('utf-8'))

producer.flush()
```

---

### Question 3: Consumer - Trip Distance

**Objective:** Validate the ingested data by consuming the topic and filtering records based on distance.

**Answer:** `8506`

**Steps:** 1. Create a Kafka Consumer subscribing to `green-trips`. 2. Set `auto_offset_reset='earliest'` to read from the beginning of the stream. 3. Initialize a counter and iterate through messages, parsing the JSON payload. 4. Increment the counter if `trip_distance > 5.0`.

**Code:**

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('green-trips', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')

count = 0
for message in consumer:
    data = json.loads(message.value)
    if data['trip_distance'] > 5.0:
        count += 1
# Note: Manually stopped after processing the dataset
```

---

### Question 4: Tumbling Window - Pickup Location

**Objective:** Calculate the number of trips per pickup location using a 5-minute tumbling window.

**Answer:** `75`

**Steps:** 1. Define the source table in PyFlink using the Kafka connector. 2. Implement **Event Time** processing by converting the pickup string to a timestamp. 3. Define a 5-minute Tumbling Window (`TUMBLE`). 4. Group by the window and `PULocationID` to count trips.

**Code:**

```sql
CREATE TABLE green_trips (
    PULocationID INT,
    lpep_pickup_datetime STRING,
    event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
    WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
) WITH (...);

SELECT PULocationID, COUNT(*) as num_trips
FROM TABLE(TUMBLE(TABLE green_trips, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTES))
GROUP BY window_start, window_end, PULocationID;
```

---

### Question 5: Session Window - Longest Streak

**Objective:** Identify the longest "streak" (most trips) within a session window defined by a 5-minute inactivity gap.

**Answer:** `51`

**Steps:** 1. Configure a Session Window in Flink with a `GAP` of 5 minutes. 2. Ensure parallelism is set to `1` so that watermarks advance correctly on the single-partition topic. 3. Sink the results to Postgres and query for the maximum count.

**Explanation:** Session windows are ideal for identifying clusters of activity. If a `PULocationID` has trips occurring within 5 minutes of each other, they belong to the same session. Once a gap exceeds 5 minutes, the session closes.

---

### Question 6: Tumbling Window - Largest Tip

**Objective:** Determine which 1-hour interval across the entire dataset generated the highest total tips.

**Answer:** `2025-10-16 18:00:00`

**Steps:** 1. Adjust the window size to `1 HOUR`. 2. Sum the `tip_amount` per window. 3. Analyze the resulting time series in PostgreSQL to find the peak hour.

---

## Key Takeaways

- **Infrastructure Parity:** Redpanda provides a seamless experience for Kafka developers with significantly less overhead and faster startup times.
- **Watermark Management:** Learned that in Flink, if parallelism is higher than the number of Kafka partitions, idle subtasks can stall the watermark, preventing windows from closing.
- **Windowing Logic:** Gained practical experience distinguishing between **Tumbling Windows** (fixed intervals) and **Session Windows** (activity-based intervals).
- **Schema Evolution:** Handling data types (like converting Parquet timestamps to JSON strings and back to Flink timestamps) is a critical part of the ETL/Streaming process.

---
