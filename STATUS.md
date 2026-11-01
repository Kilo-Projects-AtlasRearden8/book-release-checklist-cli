# STATUS

## What was built

A local-first Python CLI for authors planning a book release: `book_release`.
Tracks a checklist of tasks with optional due dates, marks tasks done/undone,
removes tasks, and exports everything to CSV. Data lives in a single local JSON
file (`book_release.json` by default, overridable with `--data`). No accounts,
no API keys, no network, no secrets or personal data.

Files:
- `pyproject.toml` — packaging; builds a wheel and provides the `book-release`
  console script entry point (`pip install .`)
- `book_release/__init__.py` — package marker
- `book_release/tasks.py` — `Task` dataclass and `TaskStore` (JSON persistence,
  done/undone/remove/export, overdue detection)
- `book_release/cli.py` — argparse CLI: add/list/done/undone/remove/export
- `book_release/__main__.py` — `python3 -m book_release` entry point
- `tests/test_tasks.py` — 15 unit tests: task logic + CLI behavior
- `README.md` — usage, example workflow, credits Asdale Dynamics, LLC
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `.gitignore` — data/CSV/pycache/build-artifact ignores
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

Or install for a `book-release` command:

```bash
pip install .
book-release --data my_book.json list
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

## Verification results

- `python3 -m unittest discover -s tests -v`: 15 tests, OK
  - 7 task-logic tests (done/undone, overdue edge cases, due-date validation,
    persistence, CSV export, remove)
  - 8 CLI tests (add/list output, done state in list, export CSV, error on
    unknown task)
- `pip install .` builds a wheel successfully and installs the `book-release`
  console script; `book-release --help` and end-to-end add/list/done/export
  work via the installed command
- No external dependencies; stdlib only; runs on Python 3.13.5

## Known gaps

- No input sanitization beyond due-date validation
- Single JSON data file; no concurrent-write locking
- Overdue status is computed against the system date at list time
