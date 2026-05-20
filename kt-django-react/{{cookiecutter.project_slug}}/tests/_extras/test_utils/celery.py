import threading
from contextlib import contextmanager
from unittest.mock import patch

import pytest

# celery.contrib.pytest provides celery_app and celery_worker fixtures.
# Importing them here makes them available project-wide without explicit conftest imports.
from celery.contrib.pytest import celery_app, celery_worker  # noqa: F401


@pytest.fixture(scope="session")
def celery_config():
    """In-memory broker/backend — unit tests never need a real Redis."""
    return {
        "broker_url": "memory://",
        "result_backend": "cache+memory://",
        "task_serializer": "json",
        "result_serializer": "json",
        "accept_content": ["json"],
    }


@contextmanager
def run_celery_task_in_background(celery_task):
    """Run ``celery_task.delay()`` in background threads instead of a real broker/worker.

    Patches ``celery_task.delay`` so each call immediately starts the task
    in a daemon thread via ``celery_task.apply()``.  The task runs in-process
    and shares the same DB and file-system state as the caller.

    Threads are joined (up to 30 s each) on exit so the block cannot return
    before all dispatched tasks have finished.
    """
    threads: list[threading.Thread] = []

    def _run_in_background(*args) -> None:
        t = threading.Thread(target=celery_task.apply, kwargs={"args": args}, daemon=True)
        t.start()
        threads.append(t)

    with patch.object(celery_task, "delay", side_effect=_run_in_background):
        yield

    for t in threads:
        t.join(timeout=30)
