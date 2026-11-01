"""Task logic for the book release checklist."""

from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timezone
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    due: Optional[str] = None
    done: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def mark_done(self) -> None:
        self.done = True

    def mark_undone(self) -> None:
        self.done = False

    def is_overdue(self) -> bool:
        if not self.due or self.done:
            return False
        return date.fromisoformat(self.due) < date.today()


class TaskStore:
    def __init__(self, path: str = "book_release.json"):
        self.path = path
        self._tasks: list[Task] = []
        self._next_id = 1
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return
        data = json.loads(content)
        self._tasks = [Task(**item) for item in data.get("tasks", [])]
        self._next_id = max([t.id for t in self._tasks], default=0) + 1

    def save(self) -> None:
        data = {"tasks": [asdict(t) for t in self._tasks]}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add(self, title: str, due: Optional[str] = None) -> Task:
        if due is not None:
            date.fromisoformat(due)
        task = Task(id=self._next_id, title=title, due=due)
        self._tasks.append(task)
        self._next_id += 1
        self.save()
        return task

    def list(self) -> list[Task]:
        return sorted(self._tasks, key=lambda t: (t.due is None, t.due or "", t.id))

    def get(self, task_id: int) -> Optional[Task]:
        for t in self._tasks:
            if t.id == task_id:
                return t
        return None

    def done(self, task_id: int) -> bool:
        task = self.get(task_id)
        if task is None:
            return False
        task.mark_done()
        self.save()
        return True

    def undone(self, task_id: int) -> bool:
        task = self.get(task_id)
        if task is None:
            return False
        task.mark_undone()
        self.save()
        return True

    def remove(self, task_id: int) -> bool:
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                self.save()
                return True
        return False

    def export_csv(self, path: str) -> int:
        count = 0
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "due", "done", "created_at"])
            for task in self.list():
                writer.writerow([task.id, task.title, task.due or "", "1" if task.done else "0", task.created_at])
                count += 1
        return count
