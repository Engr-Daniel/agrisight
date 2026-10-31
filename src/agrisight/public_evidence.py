"""Public, display-ready evidence for hosting the website without private files.

The public file holds only the bundles the website already displays: each one has
passed its adapter's hash pinning, validation, pooling and suppression. Private
aggregate JSON (for example exact rare seed-source combinations) and survey
microdata are never copied. NBS permits publishing these results with a proper
reference; the downloaded microdata are not released (owner-confirmed 2026-10-31).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache
from pathlib import Path

from agrisight import (
    conditions_reporting,
    coverage_reporting,
    crop_reporting,
    irrigation_reporting,
    seed_reporting,
    stakeholder_reporting,
)

PUBLIC_PATH = Path("public/agrisight_public_v1.json")
NAMES = ("core", "crop", "seed", "irrigation", "conditions", "coverage")
CITATION = ("National Bureau of Statistics (NBS), Nigeria. Nigeria - National Agricultural Sample "
            "Survey 2023 (NGA-NBS-NASS-2023-V01). NBS Microdata Catalogue, "
            "https://microdata.nigerianstat.gov.ng/index.php/catalog/173.")
# Field names that would indicate row-level or identifying content.
FORBIDDEN = {"hhid", "household_id", "plot_id", "s02_plotroster__id", "respondent", "interviewer",
             "latitude", "longitude", "lat", "lon", "gps", "ea", "enumeration_area", "phone"}
UNAVAILABLE = {"status": "unavailable"}


class Evidence:
    """Bundles for one script run: live adapters locally, or the public file when hosted.

    Hosting is chosen explicitly by the public entry point, never inferred from missing files.
    """

    def __init__(self, root: Path, hosted: bool = False) -> None:
        self.root = root
        self.public = (load(root) or {"core": UNAVAILABLE}) if hosted else None
        self.cache: dict[str, dict] = {}

    @property
    def hosted(self) -> bool:
        return self.public is not None

    def get(self, name: str) -> dict:
        if self.public is not None:
            return self.public.get(name, UNAVAILABLE)
        if name not in self.cache:
            self.cache[name] = self._live(name)
        return self.cache[name]

    def _live(self, name: str) -> dict:
        root = self.root
        if name == "core":
            return stakeholder_reporting.build_bundle(root)
        core = self.get("core")
        if core["status"] != "available":
            return UNAVAILABLE
        households, plots = core["activities"][0]["input_rows"], core["plots"]["total"]
        crop_yes = core["activities"][0]["yes"]
        return {
            "crop": lambda: crop_reporting.build_bundle(root, households, plots, crop_yes),
            "seed": lambda: seed_reporting.build_bundle(root, households, crop_yes),
            "irrigation": lambda: irrigation_reporting.build_bundle(root, plots),
            "conditions": lambda: conditions_reporting.build_bundle(root, households, plots, core["origin"]),
            "coverage": lambda: coverage_reporting.build_bundle(root, households),
        }[name]()


def forbidden_keys(value, path: str = "") -> list[str]:
    """Every JSON path whose key looks row-level or identifying."""
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in FORBIDDEN:
                found.append(f"{path}/{key}")
            found.extend(forbidden_keys(item, f"{path}/{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(forbidden_keys(item, f"{path}/{index}"))
    return found


def build(root: Path) -> dict:
    """Collect display bundles from verified private evidence; refuse anything else."""
    evidence = Evidence(root)
    bundles = {name: evidence.get(name) for name in NAMES}
    for name, bundle in bundles.items():
        if bundle.get("status") != "available" or bundle.get("origin") == "TEST FIXTURE":
            raise ValueError(f"{name} evidence is not reviewed and available")
    if bad := forbidden_keys(bundles):
        raise ValueError(f"Identifying fields present: {bad[:5]}")
    return {"public_evidence_version": "1.0", "citation": CITATION,
            "scope": "Display aggregates only; no NBS microdata or private aggregate files.",
            "bundles": bundles}


def write(root: Path) -> str:
    text = json.dumps(build(root), indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
    path = root/PUBLIC_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@lru_cache(maxsize=4)
def _read(path: str, mtime: float) -> str:
    return Path(path).read_text(encoding="utf-8")


def load(root: Path) -> dict | None:
    """Fresh, validated copy of the public bundles; None when absent or malformed."""
    path = root/PUBLIC_PATH
    try:
        data = json.loads(_read(str(path), path.stat().st_mtime))
        bundles = data["bundles"]
        if (data.get("public_evidence_version") != "1.0" or set(bundles) != set(NAMES)
                or forbidden_keys(bundles) or bundles["core"].get("status") != "available"):
            return None
        return bundles
    except (OSError, ValueError, KeyError, TypeError):
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print("Public evidence written; SHA256", write(args.root.resolve()))
