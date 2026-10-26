"""Smoke checks for the initial package, not a claim of system functionality."""

from agrisight import __version__
from agrisight.__main__ import main


def test_version() -> None:
    assert __version__ == "0.0.1"


def test_scaffold_message(capsys) -> None:
    main()
    output = capsys.readouterr().out
    assert "M0 scaffold" in output
    assert "not implemented" in output
