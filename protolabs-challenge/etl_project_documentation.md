# ETL Project Documentation

This document describes the current ETL pipeline, recommended improvements, and a blueprint for putting it into production.

---

## Current Pipeline Overview

### Architecture
- **Extract**: `etl/extract.py` → loads parquet file into pandas DataFrame.
- **Transform**: `etl/transform.py` → computes two derived flags (`has_unreachable_hole_warning`, `has_unreachable_hole_error`) from `holes` JSON by using specified calculations.
- **Load**: `etl/load.py` → writes DataFrame into SQLite database (`cases` table).
- **Orchestrator**: `main.py` → calls extract → transform → load sequentially.

### Initial Schema (18 columns)
- Raw parquet data with string, float, and object types.

### Final Schema (20 columns)
- Adds 2 boolean columns:
  - `has_unreachable_hole_warning`
  - `has_unreachable_hole_error`

### Diagrams
- **ETL Architecture**:
![](etl_architecture.png)
- **ERD**:
![](erd_cases.png)

---

## Improvements for Development Quality

1. **Explicit transforms & type parsing**
   - Parse datetime fields properly.
   - Replace NA checks with `pd.isna`/`pd.notna`.
   - Unit tests for JSON edge cases.

2. **Data validation / quality gates**
   - Use [Great Expectations](https://greatexpectations.io/) or `pandera` to validate schema and data ranges.

3. **incrementals**
   - Support incremental loads using `updated` watermark.

4. **Logging & observability**
   - Add structured logging with record counts, duration, and anomalies.

5. **Configuration**
   - Externalize constants to YAML or environment variables.

6. **Schema management**
   - Consider normalizing `holes` into its own table.

---

## Production Blueprint

### 1. Target Platform & Storage
- Object store (S3, GCS) for raw data.
- Postgres or data warehouse for analytics (instead of SQLite).

### 2. Orchestration & Scheduling
- Prefect or Airflow DAG:
  - Tasks: extract → transform → validate → load.
  - Schedule: hourly/daily with retries.

### 3. Containerization
Example Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install uv
RUN pip install uv

# Copy project metadata and install dependencies
COPY pyproject.toml uv.lock* ./
RUN uv pip install --system --no-cache --no-deps -r uv.lock

# Copy code
COPY etl/ etl/
COPY main.py .
ENV ETL_CONFIG=/app/config/prod.yaml

CMD ["python", "main.py"]

```

### 4. Configuration & Secrets
- YAML config for paths, thresholds, and batch sizes.
- Secrets in AWS Secrets Manager or Vault.

### 5. Deployment
- Deployment can be automatized by using Terraform.

### 6. Monitoring & Alerts
- Counters: rows_in, rows_out, warnings, errors.
- Alerts if anomalies detected.

### 7. Metadata & Lineage
- Run log table with run_id, counts, checksums.
- Optional OpenLineage/Marquez integration.

---