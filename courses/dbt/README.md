# dbt course: Zoltan Toth, *The Complete dbt Bootcamp: Zero to Hero*

Plan week 4 (Nov 16-22). Start with the free "dbt Fundamentals" course (https://www.getdbt.com/dbt-learn), then use this course for incremental models, snapshots and tests.

## Setup
- If the course uses a Snowflake trial, follow it. A trial counts as first Snowflake exposure, not as a skill to claim.
- To practise without any cloud: `uv add dbt-core dbt-duckdb` and point the profile at a local DuckDB file.
- Project A will use `dbt-athena`, so pin **dbt 1.x** there. dbt 2.0 (the Rust engine) became GA in September 2026, but not every adapter supports it yet.

## Focus on
- `ref` and `source`, and the DAG they build
- Layers: staging, intermediate, marts (the same idea as medallion)
- Materializations: view, table, incremental (`is_incremental`, `unique_key`, merge), ephemeral
- Snapshots = SCD type 2
- Generic and singular tests, unit tests, source freshness, contracts
- Jinja and macros, at a basic level; seeds; `dbt build` with selectors; docs and lineage
- CI with `state:modified` in GitHub Actions

## Skip
dbt Cloud IDE details, the Semantic Layer and MetricFlow, dbt Mesh, Python models, custom materializations, the paid certification.

## Done when you can explain without notes
- [ ] Why dbt instead of stored procedures or Spark jobs
- [ ] How an incremental model avoids duplicates, and when to run a full refresh
- [ ] How a snapshot builds SCD2 history
- [ ] Which tests you put on a fact table and why

## Progress
| Date | Section | Notes |
|---|---|---|
