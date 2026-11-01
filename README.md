# Book Release Checklist CLI

A local-first Python CLI for authors planning a book release. Track your
checklist, tasks, and dates, and export everything to CSV. No accounts, no
API keys, no network — your data stays in a single JSON file on your machine.

Built by **Dylan Asdale**, registered nurse turned AI author and founder of
**Asdale Dynamics, LLC** (Indiana, formed Oct 2026). Asdale Dynamics publishes
beginner-friendly AI education, books and guides, and practical tools. This
tool is part of that open-source catalog.

More from Asdale Dynamics: The Massive AI Manual and the hub site
dylanasdale.github.io explain AI "like a friend would": plain English, step by
step, never condescending.

## Install

Requires Python 3.9+. No external dependencies.

```bash
git clone <this-repo>
cd book-release-checklist-cli
```

Run as a module:

```bash
python3 -m book_release --data my_book.json add "Finish chapter 1" --due 2027-02-01
python3 -m book_release --data my_book.json add "Write blurb"
python3 -m book_release --data my_book.json list
python3 -m book_release --data my_book.json done 1
python3 -m book_release --data my_book.json export release_plan.csv
```

Or install it for a `book-release` command:

```bash
pip install .
book-release --data my_book.json list
```

## Example workflow

```bash
# Start a plan for your book
python3 -m book_release --data my_book.json add "Finish chapter 1" --due 2027-02-01
python3 -m book_release --data my_book.json add "Write back-cover blurb" --due 2027-02-15
python3 -m book_release --data my_book.json add "Format manuscript for KDP"

# See where things stand
python3 -m book_release --data my_book.json list

# Mark work complete as you finish it
python3 -m book_release --data my_book.json done 1

# Export to CSV to open in Excel, Google Sheets, or Numbers
python3 -m book_release --data my_book.json export release_plan.csv
```

## Commands

| Command | What it does |
|---------|--------------|
| `add TITLE [--due YYYY-MM-DD]` | Add a task with an optional due date |
| `list` | Show the checklist with status and dates |
| `done ID` | Mark a task complete |
| `undone ID` | Mark a task incomplete |
| `remove ID` | Delete a task |
| `export FILE.csv` | Export all tasks to CSV |

Data is stored in `book_release.json` by default. Use `--data` to point at a
different file per book or project.

## CSV export

```
id,title,due,done,created_at
1,Finish chapter 1,2027-02-01,1,2026-...
2,Write back-cover blurb,2027-02-15,0,2026-...
3,Format manuscript for KDP,,0,2026-...
```

Open the export in Excel, Google Sheets, or Numbers.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
