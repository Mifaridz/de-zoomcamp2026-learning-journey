-- Question 1: Counting Records
SELECT COUNT(*) AS total_records
FROM `ny_taxi_data.yellow_tripdata_2024`;

-- Question 2: Data Read Estimation
-- Disclaimer: Sandbox user (No GCS Access). Cannot create External Table.
-- The estimate for the Materialized Table is 155.12 MB, while the theoretical estimate for the External Table is 0 MB.
SELECT COUNT(DISTINCT PULocationID) AS distinct_pu_count
FROM `ny_taxi_data.yellow_tripdata_2024`;

-- Question 4: Counting Zero Fare Trips
SELECT COUNT(*) AS zero_fare_count
FROM `ny_taxi_data.yellow_tripdata_2024`
WHERE fare_amount = 0;

-- Question 5: Partitioning and Clustering
-- Strategy: Partition by Date for filter and Cluster by VendorID for sorting.
CREATE OR REPLACE TABLE `ny_taxi_data.yellow_tripdata_2024_partition`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `ny_taxi_data.yellow_tripdata_2024`;

-- Question 6: Partition Benefits

-- 1. Test on Materialized Table (Normal) - Estimate: ~310.24 MB
SELECT DISTINCT VendorID
FROM `ny_taxi_data.yellow_tripdata_2024`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- 2. Test on Partitioned Table (Optimized) - Estimate: ~26.84 MB
SELECT DISTINCT VendorID
FROM `ny_taxi_data.yellow_tripdata_2024_partition`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Question 9: Understanding Table Scans
-- Disclaimer: SELECT COUNT(*) on a native BigQuery table results in 0 bytes processed because it reads metadata.
SELECT COUNT(*) FROM `ny_taxi_data.yellow_tripdata_2024`;