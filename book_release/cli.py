"""Command line interface for the book release checklist."""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .tasks import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="book-release",
        description="Plan your book release: checklist, tasks, dates, CSV export.",
    )
    parser.add_argument("--data", default="book_release.json", help="Path to the local data file (default: book_release.json)")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title", help="Task title")
    add.add_argument("--due", help="Due date (YYYY-MM-DD)")

    sub.add_parser("list", help="List tasks")

    done = sub.add_parser("done", help="Mark a task done")
    done.add_argument("id", type=int)

    undone = sub.add_parser("undone", help="Mark a task not done")
    undone.add_argument("id", type=int)

    remove = sub.add_parser("remove", help="Remove a task")
    remove.add_argument("id", type=int)

    export = sub.add_parser("export", help="Export tasks to CSV")
    export.add_argument("file", help="Output CSV path")

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = TaskStore(args.data)

    if args.command == "add":
        task = store.add(args.title, args.due)
        print(f"Added task {task.id}: {task.title}" + (f" (due {task.due})" if task.due else ""))
    elif args.command == "list":
        tasks = store.list()
        if not tasks:
            print("No tasks yet. Add one with: book-release add 'Finish chapter 1'")
            return 0
        for task in tasks:
            status = "[x]" if task.done else "[ ]"
            due = f" due {task.due}" if task.due else ""
            overdue = " OVERDUE" if task.is_overdue() else ""
            print(f"{task.id:>3} {status} {task.title}{due}{overdue}")
    elif args.command == "done":
        if store.done(args.id):
            print(f"Task {args.id} marked done")
        else:
            print(f"Task {args.id} not found", file=sys.stderr)
            return 1
    elif args.command == "undone":
        if store.undone(args.id):
            print(f"Task {args.id} marked not done")
        else:
            print(f"Task {args.id} not found", file=sys.stderr)
            return 1
    elif args.command == "remove":
        if store.remove(args.id):
            print(f"Task {args.id} removed")
        else:
            print(f"Task {args.id} not found", file=sys.stderr)
            return 1
    elif args.command == "export":
        count = store.export_csv(args.file)
        print(f"Exported {count} tasks to {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
