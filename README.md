# Udacity-Airflow-Pipelines

This project builds an **ETL pipeline with Apache Airflow** that stages data from S3 to Redshift, transforms it into fact and dimension tables, and validates the results with data quality checks.

The DAG is fully parameterized, reusable, and scheduled to run **once per hour**.

---

## 🛠️ Custom Operators

### 1. StageToRedshiftOperator
- Loads **JSON files from S3 → Redshift** using `COPY`.
- Supports templated S3 keys (e.g. `execution_date`).
- Parameters:
  - `table`, `s3_bucket`, `s3_key`, `json_path`
  - `redshift_conn_id`, `aws_credentials_id`

### 2. LoadFactOperator
- Inserts data into **fact tables**.
- Always **append-only**.

### 3. LoadDimensionOperator
- Inserts data into **dimension tables**.
- Supports **truncate-insert** or **append-only** (via param `append_only`).

### 4. DataQualityOperator
- Runs **data quality checks** against Redshift.
- Accepts list of test cases (`check_sql`, `expected_result`).
- Fails the DAG if results don’t match expectations.

---

## ⚙️ DAG Configuration

- **Default args**:
  - `depends_on_past=False`
  - `retries=3`
  - `retry_delay=5 minutes`
  - `email_on_retry=False`
  - `catchup=False`
- **Schedule**: `@hourly`

---

## ✅ Data Quality Checks

Example checks in the DAG:
- `SELECT COUNT(*) FROM users WHERE userid IS NULL` → expect `0`
- `SELECT COUNT(*) FROM songs WHERE songid IS NULL` → expect `0`

---

## ▶️ Running the Project

1. Install [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html).
2. Place the project files under your `airflow/` directory:
   - DAG → `airflow/dags/`
   - Operators → `airflow/plugins/operators/`
   - Helpers → `airflow/helpers/`
3. Configure Airflow connections:
   - **AWS credentials** (`aws_credentials`)
   - **Redshift cluster** (`redshift`)
4. Start Airflow:
   ```bash
   airflow db init
   airflow webserver --port 8080
   airflow scheduler
