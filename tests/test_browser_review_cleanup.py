"""A browser cleanup failure must never skip cleanup of the app server."""

import importlib.util
import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

pytest.importorskip("websockets")


@pytest.mark.parametrize("timeouts", [0, 1, 2])
def test_cleanup_attempts_all_owned_processes(monkeypatch, timeouts):
    path = Path(__file__).resolve().parents[1]/"scripts/m4_browser_review.py"
    spec = importlib.util.spec_from_file_location("browser_review_cleanup", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "os", SimpleNamespace(name="nt"))
    taskkill = Mock()
    monkeypatch.setattr(module.subprocess, "run", taskkill)
    server = Mock(pid=101)
    browser = Mock(pid=102)
    for process in (server, browser):
        process.poll.return_value = None
        process.wait.return_value = 0
    if timeouts:
        browser.wait.side_effect = [subprocess.TimeoutExpired([], 5)]*timeouts + [0]
    notes = module.stop_processes([server, browser])
    assert taskkill.call_count == 2
    server.wait.assert_called_once_with(timeout=5)
    assert browser.kill.call_count == bool(timeouts)
    assert bool(notes) == (timeouts == 2)
