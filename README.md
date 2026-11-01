# Data engineering learning log

My hands-on work from a 12-week data engineering plan (26 Oct 2026 to 17 Jan 2027): course exercises, book notes and concept notes. I use it to learn tools I have not used in production yet.

This is practice, not production work. I follow each course, then redo the exercises from memory. The code shows the learning path; it is not a claim of experience.

## What's inside

| Folder | Source | What I built |
|---|---|---|
| [`courses/kafka/`](courses/kafka/) | Stephane Maarek, *Learn Apache Kafka for Beginners v3* | Python producers and consumers (callbacks, keys, consumer groups, cooperative rebalancing, graceful shutdown), a Wikimedia stream producer, and the course's CLI scripts. Kafka runs in Docker (KRaft) |
| [`courses/airflow/`](courses/airflow/) | Marc Lamberti, *The Complete Hands-On Introduction to Apache Airflow 3* | Airflow 3 DAGs in Docker Compose: a user-processing pipeline, a sales pipeline, and asset-driven DAGs |
| [`courses/dbt/`](courses/dbt/) | Zoltan Toth, *The Complete dbt Bootcamp* | The Airbnb project on Snowflake: source, dimension, fact and mart models, snapshots (SCD type 2), seeds, singular and generic tests, custom macros, `dbt_utils` and docs |
| [`notes/books/`](notes/books/) | *Fundamentals of Data Engineering*, *Designing Data-Intensive Applications*, *The Data Warehouse Toolkit* | Five lines per chapter, in my own words |
| [`notes/concepts/`](notes/concepts/) | | One note per concept (CDC, dead-letter queues, idempotency, ...) |

Each course folder has its own README: what I focused on, what I skipped, how to run it, and a checklist of what I can explain without notes.

## The plan

| Weeks | Focus |
|---|---|
| 1-2 | Kafka and stream processing |
| 3 | Airflow 3 |
| 4 | dbt and dimensional modelling |
| 5-12 | Cloud data engineering and portfolio projects |

## Portfolio projects

Projects live in their own repositories, not here. Links will appear here as they are published.

## How I learn

- Follow the lecture, then redo the exercise without looking.
- After each chapter or section, write five lines in my own words. If I cannot write them, I have not learned it yet.
- Use AI to explain and to quiz me: I try on my own first, then ask "why" questions.

Secrets, `.env` files, `profiles.yml` and course PDFs are not committed.
