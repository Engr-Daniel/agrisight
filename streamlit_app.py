"""Local aggregate evidence explorer. Run from the checkout root."""

from pathlib import Path

from agrisight.stakeholder_site import run

run(Path(__file__).resolve().parent)
