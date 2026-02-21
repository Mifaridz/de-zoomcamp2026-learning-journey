# Module 5 Homework: Data Platforms with Bruin

---

## Homework Solutions

### Question 1. Bruin Pipeline Structure

**Objective:** Understand the fundamental directory and configuration requirements for a Bruin project.

> **Answer:** `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
> **Why?** Bruin is highly flexible. The `.bruin.yml` file acts as the project root and environment configuration (like defining the DuckDB connection), while the `pipeline.yml` defines the pipeline itself. The actual SQL or Python assets can be organized however you prefer, as long as they contain the correct frontmatter to link them to the pipeline.

---

### Question 2. Materialization Strategies

**Objective:** Identify the correct incremental loading strategy for time-partitioned data.

```yaml
# Example asset frontmatter
materialization:
  type: incremental
  strategy: time_interval
  time_column: pickup_datetime
```

> **Answer:** `time_interval - incremental based on a time column`
> **Why?** When dealing with monthly NYC taxi data, a `time_interval` strategy allows the pipeline to safely delete and insert data for a specific period (e.g., just updating January 2020) without truncating the entire historical dataset or creating duplicates.

---

### Question 3. Pipeline Variables

**Objective:** Learn how to override pipeline variables via the command-line interface dynamically.

```bash
# Overriding the default array variable during execution
bruin run --var 'taxi_types=["yellow"]'

```

> **Answer:** `bruin run --var 'taxi_types=["yellow"]'`
> **Why?** Since the variable is defined as an array in the YAML configuration, you must pass the override as a valid JSON-like array string when using the `--var` flag in the CLI.

---

### Question 4. Running with Dependencies

**Objective:** Execute a specific asset along with all its downstream dependencies.

```bash
# Running an asset and everything that depends on it
bruin run ingestion/trips.py --downstream

```

> **Answer:** `bruin run ingestion/trips.py --downstream`
> **Why?** If you modify the ingestion script, you want to ensure all transformations (assets) that rely on `trips.py` are also rebuilt. The `--downstream` flag in Bruin explicitly triggers this cascading execution.

---

### Question 5. Quality Checks

**Objective:** Implement data quality constraints directly within the pipeline definition.

```yaml
# Adding a quality check in the asset frontmatter
columns:
  - name: pickup_datetime
    type: timestamp
    checks:
      - name: not_null
```

> **Answer:** `name: not_null`
> **Why?** Data quality is a first-class citizen in Bruin. The `not_null` check ensures the pipeline halts or warns if any records are missing the crucial timestamp field, preventing dirty data from flowing downstream.

---

### Question 6. Lineage and Dependencies

**Objective:** Visualize the Directed Acyclic Graph (DAG) of the data pipeline.

```bash
# Generating the dependency graph
bruin lineage

```

> **Answer:** `bruin lineage`
> **Why?** The `bruin lineage` command is essential for debugging and understanding the flow of data. It maps out how assets connect to one another based on their references.

---

### Question 7. First-Time Run

**Objective:** Ensure a clean slate when running the pipeline on a brand new database.

```bash
# Running the pipeline from scratch
bruin run --full-refresh

```

> **Answer:** `--full-refresh`
> **Why?** When initializing a new DuckDB instance, or when a massive schema change occurs, `--full-refresh` forces Bruin to ignore incremental logic, drop existing tables/views, and rebuild everything entirely from scratch.

---
