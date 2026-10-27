# Learning workspace

Hands-on work for the 12-week data engineering plan (2026-10-26 to 2027-01-17).
The plan itself lives in `~/Developer/career_development/learning/data_engineering_master_plan_2026-10.md`.

```
learning/
├── courses/        code written while following a course (one folder per course)
│   ├── kafka/      Maarek, Kafka for Beginners v3      plan weeks 1-2
│   ├── airflow/    Lamberti, Airflow 3                 plan week 3
│   └── dbt/        Toth, Complete dbt Bootcamp          plan week 4
├── projects/       portfolio projects, each its own git repo pushed to GitHub
├── notes/
│   ├── books/      chapter notes: FoDE, DDIA, Kimball
│   └── concepts/   one file per concept (CDC, DLQ, idempotency, ...)
└── materials/      course PDFs and slides (not tracked by git)
```

## How to work here
- Open one folder per VS Code window: **File > Open Folder** and pick, for example, `courses/kafka`. To use `code courses/kafka` from the terminal, run **Shell Command: Install 'code' command in PATH** once from the Command Palette (Cmd+Shift+P).
- Courses: follow the lecture, then redo the exercise yourself without looking. Course code is practice; it does not go on the CV.
- Projects: each project in `projects/` gets its own `git init` and a public GitHub repo. Commit the design doc first.
- Notes: after each chapter or lecture section, write 5 lines in your own words in `notes/`. If you cannot write them, you have not learned it yet.
- AI rule: try first for 20-30 minutes, then ask "why" questions. Never paste the whole exercise and ask for the answer.

This folder is one git repo for courses and notes. `projects/` and `materials/` are ignored here, because projects have their own repos.
