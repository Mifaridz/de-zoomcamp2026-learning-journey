# Module 1 Homework: Docker, SQL, and Terraform

## Overview
This repository contains my solutions for **Module 1** of the Data Engineering Zoomcamp. In this module, I focused on containerizing applications, setting up a local data pipeline with Postgres, and provisioning infrastructure using Terraform.

## Technologies Used
- **Docker & Docker Compose**: For containerization and orchestration.
- **PostgreSQL**: As the Data Warehouse.
- **pgAdmin**: For database management and SQL execution.
- **Python (Pandas & SQLAlchemy)**: For data ingestion.
- **Terraform**: For Infrastructure as Code (GCP).

---

## Homework Solutions

### Question 1. Understanding Docker images

**Objective:** Check the `pip` version inside the python image.
![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/01-docker-terraform/homework/homework-image/question-1.png?raw=true)

>**Answer:** `25.3`

**Steps:**
I ran the python container interactively with `bash` entrypoint to execute shell commands:
```bash
docker run -it --entrypoint bash python:3.13
```

Inside the container, I checked the version:

```bash
pip --version
# Output: pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

---

### Question 2. Understanding Docker networking and docker-compose

**Objective:** Identify the correct hostname and port for service communication.
![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/01-docker-terraform/homework/homework-image/question-2.png?raw=true)

>**Answer:** `db:5432`

**Reasoning:**
In a user-defined Docker network (created by `docker-compose`), services communicate using their **service names** as hostnames.

* Service name: `db`
* Internal container port: `5432`
* Host port mapping (5433) is only for connections from the host machine (laptop), not between containers.

---

### Data Preparation

Before solving Questions 3-6, I prepared the environment and ingested the data.

1. **Start Services:**
```bash
docker-compose up -d

```


2. **Ingest Data:**
I used a Python script (available in `ingest_data.py`) to download the *Green Taxi Trip Records (Nov 2025)* and *Taxi Zone Lookup* data, convert them to Pandas DataFrames, and load them into PostgreSQL.

---

### Question 3. Counting short trips

**Objective:** Count trips  1 mile between 2025-11-01 and 2025-12-01.
![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/01-docker-terraform/homework/homework-image/question-3.png?raw=true)

>**Answer:** `8007`

**SQL Query:**

```sql
SELECT count(1)
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;

```

---

### Question 4. Longest trip for each day

**Objective:** Find the day with the longest trip distance (filtering out outliers > 100 miles).
![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/01-docker-terraform/homework/homework-image/question-4.png?raw=true)


>**Answer:** `2025-11-14`

**SQL Query:**

```sql
SELECT
    DATE(lpep_pickup_datetime) AS pickup_day,
    MAX(trip_distance) AS max_distance
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 100
GROUP BY pickup_day
ORDER BY max_distance DESC
LIMIT 1;

```

---

### Question 5. Biggest pickup zone

**Objective:** Find the pickup zone with the largest total amount on 2025-11-18.

**Answer:** `East Harlem North`

**SQL Query:**

```sql
SELECT
    z."Zone" AS pickup_zone,
    SUM(t.total_amount) AS total_revenue
FROM green_taxi_trips t
JOIN zones z
    ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;

```

---

### Question 6. Largest tip

**Objective:** Find the drop-off zone with the largest tip for passengers picked up in "East Harlem North".

**Answer:** `JFK Airport`

**SQL Query:**

```sql
SELECT
    z_drop."Zone" AS dropoff_zone,
    t.tip_amount
FROM green_taxi_trips t
JOIN zones z_pick
    ON t."PULocationID" = z_pick."LocationID"
JOIN zones z_drop
    ON t."DOLocationID" = z_drop."LocationID"
WHERE z_pick."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01'
  AND t.lpep_pickup_datetime < '2025-12-01'
ORDER BY t.tip_amount DESC
LIMIT 1;

```

---

### Question 7. Terraform Workflow

**Objective:** Identify the correct sequence of Terraform commands.

**Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`

**Explanation:**

1. `terraform init`: Initializes the working directory and downloads providers.
2. `terraform apply -auto-approve`: Applies changes to cloud provider without asking for "yes" confirmation.
3. `terraform destroy`: Removes all resources managed by the configuration.

---

## Key Takeaways

* Learned how to inspect Docker images using entrypoint overrides.
* Understood the difference between Docker host ports and internal container ports.
* Practiced complex SQL aggregations and Joins on timestamped data.
* Gained familiarity with Terraform lifecycle commands.