# Module 04 Homework: Analytics Engineering

> **Disclaimer:** For this module, I am using a **local dbt setup** with **DuckDB** as the database engine instead of Google BigQuery. This approach allows for high-performance local transformations and efficient handling of the NYC Taxi datasets without cloud egress costs.

---

## Homework Solutions

### Question 1. dbt Lineage and Execution

**Objective:** Understand the behavior of the dbt selection flag (`--select`).

```bash
# Executing the command
dbt run --select int_trips_unioned

```

> **Answer:** `int_trips_unioned` only

> **Why?** In dbt, selecting a model by its name without graph operators (like `+` or `@`) instructs dbt to run only that specific node in the DAG. Upstream and downstream dependencies are ignored.

---

### Question 2. dbt Tests

**Objective:** Understand how dbt handles data quality test failures.

> **Answer:** `dbt will fail the test, returning a non-zero exit code`

> **Why?** Generic tests like `accepted_values` act as assertions. If the underlying query returns rows (i.e., values not in the allowed list), the test fails. dbt will then return a failure status code, which is crucial for stopping CI/CD pipelines when data quality is compromised.

---

### Question 3. Counting Records in `fct_monthly_zone_revenue`

**Objective:** Verify the final record count of the core aggregated fact table.

```sql
SELECT COUNT(*)
FROM dev.fct_monthly_zone_revenue;

```

> **Answer:** `14,120`

---

### Question 4. Best Performing Zone for Green Taxis (2020)

**Objective:** Analyze monthly revenue to find the top-performing pickup zone.

```sql
SELECT
    zone,
    revenue_monthly_total_amount
FROM fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND year = 2020
ORDER BY revenue_monthly_total_amount DESC
LIMIT 1;

```

> **Answer:** `East Harlem North`

---

### Question 5. Green Taxi Trip Counts (October 2019)

**Objective:** Extract trip volume metrics for a specific service type and timeframe.

```sql
SELECT
    SUM(total_monthly_trips) AS total_trips
FROM fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND year = 2019
  AND month = 10;

```

> **Answer:** `500,234`

---

### Question 6. Build a Staging Model for FHV Data

**Objective:** Engineer a staging pipeline for For-Hire Vehicle (FHV) data including filtering and schema standardization.

```sql
-- models/staging/stg_fhv_tripdata.sql
{{ config(materialized='view') }}

SELECT
    dispatching_base_num,
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(dropOff_datetime AS TIMESTAMP) AS dropoff_datetime,
    CAST(PUlocationID AS INTEGER) AS pickup_location_id,
    CAST(DOlocationID AS INTEGER) AS dropoff_location_id,
    SR_Flag,
    Affiliated_base_number
FROM {{ source('staging', 'fhv_tripdata') }}
WHERE dispatching_base_num IS NOT NULL;


```

> **Answer:** `43,244,693`

---
