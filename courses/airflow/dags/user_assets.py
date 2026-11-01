# ─────────────────────────────────────────────────────────────────────────────
# user_assets — the ASSET-CENTRIC way (Airflow 3's @asset decorator)
#
# In user_processing.py we wrote a DAG and TASKS, then added outlets=[...].
# Here we write the DATA we want instead. Each @asset function automatically
# becomes: one DAG + one task + one asset, all with the same name.
#
#   fake_user  ──►  user_info  ──►  user_location
#   (@daily)        (runs when        user_login
#                    fake_user        (two assets from ONE task)
#                    is updated)
# ─────────────────────────────────────────────────────────────────────────────

# `asset` (small a) = the decorator that defines an asset with code.
# `Asset` (big A)   = a plain asset name/label, like in user_processing.py.
# `Context`         = the type for the run's context (run id, task instance, ...).
from airflow.sdk import Asset, Context, asset


# ── Asset 1: fake_user ──
# This one decorator creates:
#   - a DAG named "fake_user" with schedule @daily
#   - a task named "fake_user" inside it
#   - an asset named "fake_user", updated every time that task succeeds
# uri = WHERE the data comes from. It's just information for people (and the
# function below reads it through self.uri). Airflow never opens it by itself.
@asset(
    schedule="@daily",
    uri="https://raw.githubusercontent.com/marclamberti/datasets/refs/heads/main/fakeuser.json",
)
def fake_user(self) -> dict:  # `self` = this asset itself (gives us self.name, self.uri)
    import requests  # import inside the task, not at the top (the parsing rule)

    response = requests.get(self.uri)  # download the JSON from the uri above
    response.raise_for_status()        # if the API returned an error (4xx/5xx) → fail the task
    # The returned value is saved in XCom. That's how downstream assets get the data.
    return response.json()


# ── Assets 2 and 3: user_location and user_login ──
# @asset.multi = ONE task that produces SEVERAL assets (listed in outlets).
# schedule=fake_user → run every time the fake_user asset gets a new event.
@asset.multi(
    schedule=fake_user,
    outlets=[Asset("user_location"), Asset("user_login")],
)
# The parameter is named `fake_user` → Airflow gives us the fake_user ASSET.
# Careful: we get the asset (its name/uri), NOT the data itself.
def user_info(fake_user: Asset, context: Context) -> list[dict]:
    # The data lives in the XCom of ANOTHER DAG run (fake_user's run), not this one.
    # So first: find WHICH run produced it.
    # triggering_asset_events = the asset events that started this run.
    # Each event remembers its source: source_dag_id, source_task_id, source_run_id.
    # [-1] = the newest event (if fake_user updated twice, events collapse into one run).
    event = context["triggering_asset_events"][fake_user][-1]

    # Now pull the XCom from exactly that run.
    # dag_id and task_ids are both "fake_user" because @asset used the same name for all.
    # (Many tutorials use include_prior_dates=True instead. In Airflow 3 that fails
    #  here: it compares logical dates, and manual/asset-triggered runs have NONE.)
    user_data = context["ti"].xcom_pull(
        dag_id=fake_user.name,
        task_ids=fake_user.name,
        run_id=event.source_run_id,
    )

    # Return one value per outlet, in the same order: [user_location, user_login]
    return [
        user_data["personalInfo"]["address"],  # → user_location
        user_data["accountDetails"],           # → user_login
    ]
