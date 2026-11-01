# ─────────────────────────────────────────────────────────────────────────────
# user_report — the CONSUMER DAG
# It has no time schedule. It starts automatically every time the asset
# `users` gets a new event (when user_processing.store_user succeeds).
# ─────────────────────────────────────────────────────────────────────────────

from airflow.sdk import Asset, dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

# The SAME name as in user_processing.py → it is the SAME asset.
# This string is the only link between the two DAGs; they don't import each other.
users_asset = Asset("users")


# schedule=[users_asset] → "run me when `users` is updated" (instead of "@daily").
# A list means AND: with several assets, ALL must be updated before a run starts.
@dag(schedule=[users_asset])
def user_report():

    @task
    def count_users():
        # Same Connection as the producer — the hook logs in to Postgres for us.
        hook = PostgresHook(postgres_conn_id="postgres")
        # get_first() runs the query and returns the FIRST row as a tuple, e.g. (1,)
        # [0] takes the first column of that row → the number.
        count = hook.get_first("SELECT COUNT(*) FROM users")[0]
        print(f"We now have {count} users")  # shows up in this task's log

    count_users()  # calling the @task function inside the DAG creates the task


user_report()  # register the DAG
