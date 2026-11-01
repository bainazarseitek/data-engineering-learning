# ─────────────────────────────────────────────────────────────────────────────
# user_processing — the PRODUCER DAG
# Gets one fake user from an API, saves it to a CSV, loads the CSV into Postgres.
# When the load succeeds, it "rings the bell" for the asset `users`,
# so the consumer DAG (user_report) starts automatically.
#
# Pipeline:
#   create_table → is_api_available → extract_user → process_user → store_user
# ─────────────────────────────────────────────────────────────────────────────

# `dag` and `task` are decorators that turn Python functions into a DAG and tasks.
# `Asset` is the "name on the bell" — a label for a piece of data.
from airflow.sdk import Asset, dag, task

# A ready-made OPERATOR (from the common-sql PROVIDER) that runs one SQL statement.
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# The object a sensor returns: "am I done?" + an optional value to pass on via XCom.
from airflow.sdk.bases.sensor import PokeReturnValue

# A HOOK (a client) from the postgres PROVIDER. It logs in to Postgres using
# the Airflow Connection, so no password is written in this file.
from airflow.providers.postgres.hooks.postgres import PostgresHook

# The asset this DAG produces. Only the NAME matters — "users".
# Airflow never looks at the real table; it trusts our announcement.
users_asset = Asset("users")

# The CSV columns, in the SAME ORDER as the table columns.
# Postgres COPY loads columns by POSITION, not by name, so the order must match.
USER_COLUMNS = ["id", "firstname", "lastname", "email", "created_at"]


@dag  # no schedule given → schedule=None → runs only when triggered (manually or by API)
def user_processing():  # the function name becomes the dag_id: "user_processing"

    # Task 1: make sure the table exists.
    # This is an OPERATOR task: we only fill in parameters, the operator does the work.
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",  # the name shown in the UI
        conn_id="postgres",      # which Airflow Connection to use (Admin → Connections)
        # IF NOT EXISTS → safe to run many times (it does nothing if the table is already there)
        sql="""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    )

    # Task 2: a SENSOR — it waits until the API answers.
    # poke_interval=30 → check every 30 seconds
    # timeout=300      → give up (fail) after 5 minutes
    @task.sensor(poke_interval=30, timeout=300)
    def is_api_available() -> PokeReturnValue:
        # Import INSIDE the task, not at the top of the file: the DAG processor
        # re-reads this file every ~30 s, and we don't want extra work each time.
        import requests

        response = requests.get(
            "https://raw.githubusercontent.com/marclamberti/datasets/refs/heads/main/fakeuser.json"
        )
        print(response.status_code)  # print() goes to the task log in the UI

        if response.status_code == 200:  # 200 = "OK", the API works
            condition = True             # the sensor is done
            fake_user = response.json()  # the JSON becomes a Python dict
        else:
            condition = False            # not done → Airflow tries again in 30 s
            fake_user = None

        # is_done   → tells Airflow whether to stop waiting
        # xcom_value → saved in XCom, so the next task receives it as its argument
        return PokeReturnValue(is_done=condition, xcom_value=fake_user)

    # Task 3: keep only the fields we need from the big JSON.
    @task
    def extract_user(fake_user):  # `fake_user` = the sensor's xcom_value (Airflow loads it from XCom)
        # The returned dict is saved as this task's XCom ("return_value").
        return {
            "id": fake_user["id"],
            "firstname": fake_user["personalInfo"]["firstName"],
            "lastname": fake_user["personalInfo"]["lastName"],
            "email": fake_user["personalInfo"]["email"],
        }

    # Task 4: write the user to a CSV file.
    @task
    def process_user(user_info):  # `user_info` = extract_user's returned dict (from XCom)
        import csv
        from datetime import datetime

        # Add the time we processed this user.
        user_info["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # /tmp only works because LocalExecutor runs all tasks in ONE container.
        # With many workers, store_user could run on another machine and not find this file.
        with open("/tmp/user_info.csv", "w", newline="") as f:
            # BUG FIX: fieldnames=USER_COLUMNS fixes the column order.
            # Before, we used user_info.keys(). But XCom is stored in Postgres JSONB,
            # and JSONB does NOT keep key order — so email ended up in firstname.
            writer = csv.DictWriter(f, fieldnames=USER_COLUMNS)
            writer.writeheader()      # first line: id,firstname,lastname,email,created_at
            writer.writerow(user_info)  # second line: the values, in the same order

    # Task 5: load the CSV into Postgres.
    # outlets=[users_asset] → when THIS task SUCCEEDS, Airflow records an
    # asset event "users was updated". If it fails, no event, no consumer run.
    @task(outlets=[users_asset])
    def store_user():
        # The hook reads host/login/password from the "postgres" Connection.
        hook = PostgresHook(postgres_conn_id="postgres")
        # COPY = Postgres's fast bulk load. HEADER → skip the first line of the CSV.
        hook.copy_expert(
            sql="COPY users FROM STDIN WITH CSV HEADER",
            filename="/tmp/user_info.csv",
        )

    # ── Dependencies (the arrows) ──
    # Read from the inside out:
    #   create_table >> is_api_available()  → the sensor runs after create_table
    #   extract_user(...)                   → gets the sensor's XCom (this also makes an arrow)
    #   process_user(...)                   → gets extract_user's XCom (arrow)
    #   >> store_user()                     → no data passed, so we draw the arrow with >>
    process_user(extract_user(create_table >> is_api_available())) >> store_user()


# Call the function so Airflow registers the DAG when it parses this file.
user_processing()
