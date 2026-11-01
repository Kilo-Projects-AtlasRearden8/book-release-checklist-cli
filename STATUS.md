# STATUS

## What was built

A local-first Python CLI for authors planning a book release: `book_release`.
Tracks a checklist of tasks with optional due dates, marks tasks done/undone,
removes tasks, and exports everything to CSV. Data lives in a single local JSON
file (`book_release.json` by default, overridable with `--data`). No accounts,
no API keys, no network, no secrets or personal data.

Files:
- `book_release/__init__.py` — package marker
- `book_release/tasks.py` — `Task` dataclass and `TaskStore` (JSON persistence,
  done/undone/remove/export, overdue detection)
- `book_release/cli.py` — argparse CLI: add/list/done/undone/remove/export
- `book_release/__main__.py` — `python3 -m book_release` entry point
- `tests/test_tasks.py` — 11 unit tests for task logic (unittest, stdlib only)
- `README.md` — usage, credits Asdale Dynamics, LLC
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `.gitignore` — data/CSV/pycache ignores
- `STATUS.md` — this file

## How to run it

Requires Python 3.9+. No external dependencies.

```bash
cd /workspace/kilo-lab/book-release-checklist-cli
python3 -m book_release --data my_book.json add "Finish chapter 1" --due 2027-02-01
python3 -m book_release --data my_book.json add "Write blurb"
python3 -m book_release --data my_book.json list
python3 -m book_release --data my_book.json done 1
python3 -m book_release --data my_book.json export release_plan.csv
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

## Verification results

- `python3 -m unittest discover -s tests -v`: 11 tests, OK
- CLI end-to-end smoke test: add 2 tasks, list shows both with due dates,
  `done 1` marks complete, `export` writes CSV with header
  `id,title,due,done,created_at` and correct rows
- No external dependencies; runs on Python 3.13.5 with stdlib only

## Known gaps

- No packaging (`pyproject.toml`/`setup.py`) or `console_scripts` entry point;
  invoke via `python3 -m book_release`
- No input sanitization beyond due-date validation
- Single JSON data file; no concurrent-write locking
- Overdue status is computed against the system date at list time
