"""Repository research explorer, separate from the stakeholder website."""
from pathlib import Path

from agrisight.reporting_ui import run

run(Path(__file__).resolve().parent)
