"""Tests for task logic."""

from __future__ import annotations

import csv
import io
import os
import tempfile
import unittest
from unittest.mock import patch
from datetime import date, timedelta

from book_release.cli import main
from book_release.tasks import Task, TaskStore


class TestTask(unittest.TestCase):
    def test_mark_done_and_undone(self):
        task = Task(id=1, title="Write chapter 1")
        self.assertFalse(task.done)
        task.mark_done()
        self.assertTrue(task.done)
        task.mark_undone()
        self.assertFalse(task.done)

    def test_is_overdue_when_due_date_passed(self):
        task = Task(id=1, title="x", due=(date.today() - timedelta(days=1)).isoformat())
        self.assertTrue(task.is_overdue())

    def test_not_overdue_when_done(self):
        task = Task(id=1, title="x", due=(date.today() - timedelta(days=1)).isoformat(), done=True)
        self.assertFalse(task.is_overdue())

    def test_not_overdue_when_no_due_date(self):
        task = Task(id=1, title="x")
        self.assertFalse(task.is_overdue())

    def test_is_not_overdue_when_due_today(self):
        task = Task(id=1, title="x", due=date.today().isoformat())
        self.assertFalse(task.is_overdue())


class TestTaskStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.store = TaskStore(self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_add_and_list(self):
        self.store.add("Draft cover", due="2027-01-01")
        self.store.add("Write blurb")
        tasks = self.store.list()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Draft cover")
        self.assertEqual(tasks[1].title, "Write blurb")
        self.assertIsNone(tasks[1].due)

    def test_add_validates_due_date(self):
        with self.assertRaises(ValueError):
            self.store.add("x", due="not-a-date")

    def test_done_and_undone(self):
        self.store.add("Task")
        self.assertTrue(self.store.done(1))
        self.assertTrue(self.store.get(1).done)
        self.assertTrue(self.store.undone(1))
        self.assertFalse(self.store.get(1).done)
        self.assertFalse(self.store.done(999))
        self.assertFalse(self.store.undone(999))

    def test_persistence(self):
        self.store.add("Persist me")
        store2 = TaskStore(self.tmp.name)
        self.assertEqual(len(store2.list()), 1)
        self.assertEqual(store2.list()[0].title, "Persist me")

    def test_export_csv(self):
        self.store.add("Task A", due="2027-02-01")
        self.store.add("Task B")
        self.store.done(1)
        path = self.tmp.name + ".csv"
        count = self.store.export_csv(path)
        self.assertEqual(count, 2)
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[0], ["id", "title", "due", "done", "created_at"])
        self.assertEqual(rows[1][0], "1")
        self.assertEqual(rows[1][3], "1")
        os.unlink(path)

    def test_remove(self):
        self.store.add("A")
        self.store.add("B")
        self.assertTrue(self.store.remove(1))
        self.assertIsNone(self.store.get(1))
        self.assertEqual(len(self.store.list()), 1)
        self.assertFalse(self.store.remove(999))


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def _run(self, *args):
        argv = ["--data", self.tmp.name, *args]
        buf = io.StringIO()
        with patch("sys.stdout", buf), patch("sys.stderr", buf):
            code = main(argv)
        return code, buf.getvalue()

    def test_add_and_list_output(self):
        code, out = self._run("add", "Finish chapter 1", "--due", "2027-02-01")
        self.assertEqual(code, 0)
        code, out = self._run("list")
        self.assertEqual(code, 0)
        self.assertIn("Finish chapter 1", out)
        self.assertIn("2027-02-01", out)

    def test_done_then_list_shows_checked(self):
        self._run("add", "Task one")
        self._run("done", "1")
        code, out = self._run("list")
        self.assertEqual(code, 0)
        self.assertIn("[x]", out)

    def test_export_writes_csv(self):
        self._run("add", "Task A", "--due", "2027-02-01")
        csv_path = self.tmp.name + ".csv"
        code, out = self._run("export", csv_path)
        self.assertEqual(code, 0)
        with open(csv_path, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[0], ["id", "title", "due", "done", "created_at"])
        os.unlink(csv_path)

    def test_unknown_task_errors(self):
        code, out = self._run("done", "999")
        self.assertEqual(code, 1)
        self.assertIn("not found", out)

