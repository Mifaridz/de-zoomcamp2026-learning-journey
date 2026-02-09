# Module 3 Homework: Data Warehouse

## Overview

This repository contains my solutions for **Module 3** of the Data Engineering Zoomcamp. This module focused on **Data Warehousing** using **Google BigQuery**. The key objectives were to understand BigQuery's architecture, storage efficiency (Columnar Storage), and query optimization techniques such as **Partitioning** and **Clustering**.

## ⚠️ Special Note: Environment & Workaround

Since my _GCP Free Trial_ had expired, I did not have access to create a **GCP Bucket (GCS)** due to billing requirements. To overcome this, I utilized the **BigQuery Sandbox** and implemented the following workaround:

1. **Local Data Acquisition**: Downloaded the 6 Parquet files (January - June 2024) directly to my local machine.
2. **Google Cloud SDK**: Used the `bq load` CLI tool to upload data from my local environment directly into BigQuery as **Native Tables**.
3. **Optimization**: Performed data transformations within BigQuery to create partitioned and clustered tables to meet the homework requirements.

## Technologies Used

- **Google BigQuery**: Primary Data Warehouse.
- **Google Cloud SDK (CLI)**: For loading local data to the cloud without GCS.
- **SQL**: For data analysis, schema management, and optimization.

---

## Homework Solutions

### Question 1. What is count of records for the 2024 Yellow Taxi Data?

**Objective:** Determine the total number of records for the period January - June 2024.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/03-data-warehouse/Homework/Homework-image/question-1.png?raw=true)

```sql
SELECT COUNT(*) AS total_records
FROM `ny_taxi_data.yellow_tripdata_2024`;

```

> **Answer:** `20,332,093`

---

### Question 2. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

**Objective:** Compare scan costs between an External Table (GCS) and a Materialized Table (Native BQ Storage).

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/03-data-warehouse/Homework/Homework-image/question-2.png?raw=true)

```sql
-- Executed on the Materialized Table
SELECT COUNT(DISTINCT PULocationID)
FROM `ny_taxi_data.yellow_tripdata_2024`;

```

> **Answer:** `0 MB for the External Table and 155.12 MB for the Materialized Table`
> _Note: Since I am using the Sandbox, the External Table estimate is based on the theoretical behavior where BQ does not scan external file metadata before the query execution._

---

### Question 3. Why are the estimated number of Bytes different?

**Objective:** Understand the mechanics of **Columnar Storage**.

> **Answer:** `BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.`

- https://docs.cloud.google.com/bigquery/docs/storage_overview
- https://docs.cloud.google.com/bigquery/docs/storage_overview#storage_layout

---

### Question 4. How many records have a fare_amount of 0?

**Objective:** Filter data based on specific criteria.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/03-data-warehouse/Homework/Homework-image/question-4.png?raw=true)

```sql
SELECT COUNT(*)
FROM `ny_taxi_data.yellow_tripdata_2024`
WHERE fare_amount = 0;

```

> **Answer:** `8,333`

---

### Question 5. What is the best strategy to make an optimized table in Big Query?

**Objective:** Determine the ideal Partitioning and Clustering strategy for time-based filtering and Vendor-based sorting.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/03-data-warehouse/Homework/Homework-image/question-5.png?raw=true)

```sql
CREATE OR REPLACE TABLE `ny_taxi_data.yellow_tripdata_2024_partition`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `ny_taxi_data.yellow_tripdata_2024`;

```

> **Answer:** `Partition by tpep_dropoff_datetime and Cluster on VendorID`

---

### Question 6. What are these values (Estimated bytes processed)?

**Objective:** Prove the efficiency of Partitioning.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/03-data-warehouse/Homework/Homework-image/question-6.png?raw=true)

```sql
-- Comparing estimated bytes between:
-- 1. Materialized Table (Normal)
SELECT DISTINCT VendorID FROM `ny_taxi_data.yellow_tripdata_2024`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- 2. Partitioned Table (Optimized)
SELECT DISTINCT VendorID FROM `ny_taxi_data.yellow_tripdata_2024_partition`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

```

> **Answer:** `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`

---

### Question 7. Where is the data stored in the External Table you created?

**Objective:** Understand external data storage locations.

> **Answer:** `GCP Bucket`

- https://docs.cloud.google.com/bigquery/docs/external-tables

---

### Question 8. It is best practice in Big Query to always cluster your data?

**Objective:** Understand when to apply Clustering.

> **Answer:** `False`
> _Note: Clustering is generally not recommended for tables smaller than 1 GB, as the metadata overhead can outweigh the performance benefits._

---

### Question 9. Write a SELECT count(\*) query. How many bytes does it estimate?

**Objective:** Understand BigQuery metadata optimization.

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/03-data-warehouse/Homework/Homework-image/question-9.png?raw=true)

```sql
SELECT COUNT(*) FROM `ny_taxi_data.yellow_tripdata_2024`;

```

> **Answer:** `0 Bytes`
> **Why?** BigQuery stores the row count in the table's metadata. A `COUNT(*)` query on a native table retrieves this pre-calculated value without scanning the actual data blocks.

---

### Final Reflection

Using the **BigQuery Sandbox** required more manual effort (local CLI uploads), but it provided a deeper understanding of how BigQuery manages internal storage versus external references. This constraint turned out to be a great learning experience in managing data warehouse resources efficiently.

---
