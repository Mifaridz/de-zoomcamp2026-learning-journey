# Module 2 Homework: Workflow Orchestration with Kestra

## Overview

This repository contains my solutions for **Module 2** of the Data Engineering Zoomcamp. This module focused on **Workflow Orchestration**, where I learned to automate, schedule, and backfill data pipelines using **Kestra**. I also practiced connecting Kestra with PostgreSQL and handling dynamic variables in ETL flows.

## Technologies Used

- **Kestra**: For workflow orchestration and pipeline management.
- **Docker & Docker Compose**: To run Kestra and PostgreSQL in a containerized environment.
- **PostgreSQL**: As the target database (Data Warehouse) for NYC Taxi data.
- **pgAdmin**: For verifying data integrity and executing SQL queries.
- **Pebble Templates**: For dynamic variable rendering within Kestra flows.

---

## Homework Solutions

### Question 1. Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size?

**Objective:** Find the size of the output file `yellow_tripdata_2020-12.csv` after the extraction task.

```yaml
- id: extract
  type: io.kestra.plugin.scripts.shell.Commands
  outputFiles:
    - "*.csv"
  taskRunner:
    type: io.kestra.plugin.core.runner.Process
  commands:
    - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{inputs.taxi}}/{{render(vars.file)}}.gz | gunzip > {{render(vars.file)}}
    - du -b {{render(vars.file)}} | awk '{printf "%.1f MiB\n", $1/1048576}' # Compute the uncompressed file size in MiB
```

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/02-workflow-orchestration/Homework/Homework-image/question-1.png?raw=true)

> **Answer:** `128.3 MiB`

**Steps:**

1. I executed the flow manually in Kestra with the following inputs: `taxi: yellow`, `year: 2020`, `month: 12`.
2. After the flow finished successfully, I navigated to the **Outputs** tab.
3. In the `extract` task outputs, I inspected the file metadata which showed the uncompressed size as 128.3 MiB.

---

### Question 2. What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04`?

**Objective:** Understand how Kestra renders Pebble templates.

```yaml
variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv" # Defines the filename pattern; used to verify variable rendering
  staging_table: "public.{{inputs.taxi}}_tripdata_staging"
  table: "public.{{inputs.taxi}}_tripdata"
  data: "{{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ inputs.year ~ '-' ~ inputs.month ~ '.csv']}}"
```

![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/02-workflow-orchestration/Homework/Homework-image/question-2.png?raw=true)

> **Answer:** `green_tripdata_2020-04.csv`

**Reasoning:**
Kestra uses Pebble templates to dynamically build strings. Given the expression:
`{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`

The variables are replaced as follows:

- `{{inputs.taxi}}` → `green`
- `{{inputs.year}}` → `2020`
- `{{inputs.month}}` → `04`
  Resulting in: `green_tripdata_2020-04.csv`

---

### Data Preparation (Backfilling)

Before solving Questions 3-5, I performed a **Backfill** operation in Kestra to ingest the historical data for the years 2020 and 2021 into my PostgreSQL database.

1. **Service Configuration:** I ensured Kestra was connected to Postgres using the hostname `pgdatabase` (as defined in my `docker-compose.yml`).
2. **Backfill Execution:** I used the Kestra Backfill feature for both `yellow` and `green` taxi types for the requested time periods.

---

### Question 3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

**Objective:** Count the total records for Yellow Taxi in 2020.
![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/02-workflow-orchestration/Homework/Homework-image/question-3.png?raw=true)

> **Answer:** `24,648,499`

**SQL Query:**

```sql
SELECT count(*) as total_rows
FROM public.yellow_tripdata
WHERE filename LIKE 'yellow_tripdata_2020-%';
```

---

### Question 4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?

**Objective:** Count the total records for Green Taxi in 2020.
![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/02-workflow-orchestration/Homework/Homework-image/question-4.png?raw=true)

> **Answer:** `1,734,051`

**SQL Query:**

```sql
SELECT count(*) as total_rows
FROM public.green_tripdata
WHERE filename LIKE 'green_tripdata_2020-%';
```

---

### Question 5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

**Objective:** Count records for a specific month in 2021.
![alt text](https://github.com/Mifaridz/de-zoomcamp2026-learning-journey/blob/main/02-workflow-orchestration/Homework/Homework-image/question-5.png?raw=true)

> **Answer:** `1,925,152`

**SQL Query:**

```sql
SELECT count(*) as total_rows
FROM public.yellow_tripdata
WHERE filename = 'yellow_tripdata_2021-03.csv';

```

---

### Question 6. How would you configure the timezone to New York in a Schedule trigger?

**Objective:** Identify the correct way to set timezones in Kestra schedules.

```yaml
triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    timezone: America/New_York # IANA timezone identifier; handles DST offsets automatically for New York
    inputs:
      taxi: green

  - id: yellow_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 10 1 * *"
    timezone: America/New_York #  IANA timezone identifier; handles DST offsets automatically for New York
    inputs:
      taxi: yellow
```

> **Answer:** `Add a timezone property set to America/New_York in the Schedule trigger configuration`

**Explanation:**
Kestra's `Schedule` trigger supports a `timezone` property that accepts IANA timezone identifiers. Using `America/New_York` is the standard way to ensure the schedule accounts for New York's local time, including Daylight Saving Time adjustments.

---

## Key Takeaways

- **Orchestration Efficiency**: Learned how **Backfilling** eliminates the need for manual repetitive tasks when dealing with historical data.
- **Network Communication**: Reaffirmed that containers within the same Docker network communicate via **Service Names** (`pgdatabase`) rather than `localhost`.
- **Dynamic Templating**: Gained proficiency in using Pebble templates and null-coalescing operators (`??`) to make flows compatible with both manual and scheduled executions.
- **Separation of Concerns**: Understood the importance of separating the orchestrator's internal database (`kestra_postgres`) from the actual data warehouse (`pgdatabase`).

---
