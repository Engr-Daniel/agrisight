"""Public hosted website: display aggregates from public/, no private evidence needed."""

from pathlib import Path

from agrisight.stakeholder_site import run

run(Path(__file__).resolve().parent, hosted=True)
