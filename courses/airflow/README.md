# Airflow course: Marc Lamberti, *The Complete Hands-On Introduction to Apache Airflow 3*

Plan week 3 (Nov 9-15). Add the free Astronomer Academy "Airflow 101" path: https://academy.astronomer.io/path/airflow-101

## Setup
Use the setup the course uses (Astro CLI or Docker Compose); both run Airflow in Docker. Learn **Airflow 3 only**. Current release: 3.3.2. If a tutorial shows SubDAGs, "datasets" or the old UI, it is Airflow 2, so skip it.

## Focus on
- How Airflow 3 is built: scheduler, DAG processor, API server, Task SDK
- TaskFlow API, retries and timeouts, connections and hooks
- Idempotent tasks, `logical_date` and data intervals, catchup and backfills
- Dynamic task mapping; assets and asset-driven scheduling
- XCom limits: pass references, never large data
- Airflow 2 vs 3 differences (a common interview question)

## Skip
Helm and Kubernetes deployment, writing custom providers, deep Celery tuning, managed Airflow on AWS (MWAA costs about $350 a month).

## Done when you can explain without notes
- [ ] Why use an orchestrator instead of cron
- [ ] When NOT to use Airflow (streaming, sub-minute latency, moving data through XCom)
- [ ] How to backfill 3 months safely, and what makes a task idempotent
- [ ] Airflow vs Dagster vs Prefect in two sentences each

## Progress
| Date | Section | Notes |
|---|---|---|
