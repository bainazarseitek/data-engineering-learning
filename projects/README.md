# Portfolio projects

Each project is its own git repository and its own public GitHub repo. Create the folder when the project starts, not before.

| Folder | Plan weeks | What | Status |
|---|---|---|---|
| `wiki-pulse/` | W1-W2 (Oct 26 - Nov 8) | Live Wikimedia edits through Kafka; crash-and-restart test with 0 duplicates; Debezium CDC lab | Not started |
| `zakup-lake/` | W3-W9 (Nov 9 - Dec 27) | Kazakhstan public procurement lakehouse on AWS: Airflow, Kafka change stream, S3/Athena/Iceberg, dbt, Terraform, CI | Waiting for the goszakup token (fallback: ProZorro) |
| `zakup-analyst/` | W10-W12 (Dec 28 - Jan 17) | Text-to-SQL and metadata agent in Russian, Kazakh and English on top of zakup-lake; FastAPI, guardrails, eval set | Not started |

Full specs: `~/Developer/career_development/research_notes/Data engineering learning plan/portfolio_projects.md` § 4.

## Starting a project
```bash
mkdir wiki-pulse && cd wiki-pulse && git init
mkdir -p docs/adr && touch docs/design.md docs/failure_log.md
# Write docs/design.md first and commit it before any code
```

## Every repo has
- `docs/design.md`: goals, non-goals, sources, architecture, cost ceiling (committed first)
- `docs/adr/`: one file per decision (context, options, decision, consequences)
- `docs/failure_log.md`: every real bug, its root cause and the fix
- a README with the outcome and the numbers on the first screen, a diagram, one-command run, and a "How I used AI" section
- small commits with real messages
