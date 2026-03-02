# Module — dlt Workshop: Build Your Own Pipeline

## Overview

This repository contains my solutions for the **DLT Workshop** from the DataTalksClub Zoomcamp.
In this module, I learned how to:

- Build and execute a **dlt pipeline**
- Inspect pipeline results using the **dlt Dashboard**
- Interact with my pipeline via the **dlt MCP Server agent**
- Explore and visualize the loaded data using a **Marimo Notebook**

The exercises focused on querying the Yellow Taxi dataset loaded through the `taxi_pipeline`.

---

## Technologies Used

- **dlt**: For ingestion, schema creation, and incremental loading.
- **DuckDB / BigQuery** (depending on setup): As the destination warehouse.
- **dlt Dashboard**: For exploring pipeline runs and tables.
- **dlt MCP Server**: To ask questions about the pipeline programmatically.
- **Marimo Notebook**: For running SQL queries and building visualizations.

---

## Homework Solutions

### Question 1. What is the start date and end date of the dataset?

**Objective:** Identify the earliest and latest timestamps in the loaded Yellow Taxi data.

Using tools such as the **dlt Dashboard**, the **MCP agent**, or a **Marimo SQL query** like:

```sql
SELECT
    MIN(tpep_pickup_datetime) AS start_date,
    MAX(tpep_dropoff_datetime) AS end_date
FROM trips;
```

I determined the dataset range.

> **Answer:** `2009-01-01 to 2009-01-31`

**Explanation:**
The workshop pipeline loads the January 2009 Yellow Taxi dataset, which spans exactly these dates.

---

### Question 2. What proportion of trips are paid with credit card?

**Objective:** Calculate the share of credit card payments in the loaded data.

Example query used in the notebook:

```sql
SELECT
    payment_type,
    COUNT(*) AS trips,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER() AS proportion
FROM trips
GROUP BY payment_type;
```

> **Answer:** `36.66%`

**Explanation:**
The dataset shows that approximately one-third of all trips were paid via credit card.

---

### Question 3. What is the total amount of money generated in tips?

**Objective:** Sum all tip amounts for the dataset.

Sample query:

```sql
SELECT SUM(tip_amount) AS total_tips
FROM trips;
```

> **Answer:** `$8,063.41`

**Explanation:**
The aggregated tip amount across all January 2009 trips is roughly **8k USD**.

---

## Data Exploration Notes

Throughout the workshop, I experimented with:

1. **dlt Dashboard**
   - Used `dlt pipeline taxi_pipeline show` to review table schemas and row counts.

2. **MCP Server**
   - Asked questions like _“How many trips used credit cards?”_ and received instant answers.

3. **Marimo Notebook**
   - Queried my warehouse and built small visualizations to inspect distributions such as trip distances and payment types.

---

## Key Takeaways

- **Unified Tooling:** dlt provides ingestion, schema evolution, and monitoring in one workflow.
- **Flexible Exploration:** Having three ways to inspect data (Dashboard, MCP Agent, Notebook) made validation easier.
- **Pipeline Simplicity:** The workshop showed how minimal code is required to build repeatable ingestion flows.
- **Clear Data Insights:** Simple SQL queries were enough to answer all homework questions once the pipeline was set up correctly.
