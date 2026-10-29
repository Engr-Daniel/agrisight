"""SYNTHETIC DEMONSTRATION DATA: fixed matching baselines and labelled evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sqlite3
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path

RULES = ("missing_name", "missing_contact", "name_whitespace", "contact_whitespace")
CONFIGS = ("Clean", "Exact-repeat", "Mixed")
DEVELOPMENT_SEEDS = (101, 202)
EVALUATION_SEEDS = (303, 404, 505)


@dataclass(frozen=True)
class Observation:
    submission_id: str
    name_token: str | None
    contact_token: str | None
    role_kind: str
    status: str


@dataclass(frozen=True)
class Truth:
    submission_id: str
    true_person_id: str
    true_role_id: str
    scenario: str
    defect_labels: tuple[str, ...] = ()


def validate(observations: list[Observation], truth: list[Truth]) -> None:
    ids = set()
    for row in observations:
        if not isinstance(row.submission_id, str) or not row.submission_id.strip():
            raise ValueError("Missing submission ID")
        if row.submission_id in ids:
            raise ValueError("Duplicate submission ID")
        ids.add(row.submission_id)
        if row.role_kind not in ("farmer", "processor") or row.status not in (
            "pending", "accepted", "rejected"
        ):
            raise ValueError("Unsupported role/status")
        if any(v is not None and not isinstance(v, str)
               for v in (row.name_token, row.contact_token)):
            raise ValueError("Tokens must be strings or null")
    indexed = {r.submission_id: r for r in observations}
    if len({t.submission_id for t in truth}) != len(truth) or {
        t.submission_id for t in truth
    } != ids:
        raise ValueError("Truth must cover observations exactly once")
    roles, person_roles = {}, {}
    for t in truth:
        if any(not isinstance(v, str) or not v.strip()
               for v in (t.true_person_id, t.true_role_id, t.scenario)):
            raise ValueError("Missing truth identity/scenario")
        if len(set(t.defect_labels)) != len(t.defect_labels) or not set(
            t.defect_labels
        ).issubset(RULES):
            raise ValueError("Invalid defect labels")
        owner = (t.true_person_id, indexed[t.submission_id].role_kind)
        if roles.setdefault(t.true_role_id, owner) != owner:
            raise ValueError("Conflicting intended role")
        if person_roles.setdefault(owner, t.true_role_id) != t.true_role_id:
            raise ValueError("Multiple intended roles for same person/kind")


def generate(seed: int, configuration: str) -> tuple[list[Observation], list[Truth]]:
    """Fixed 1000-person accuracy workload; no actual identities or survey inputs."""
    if type(seed) is not int or configuration not in CONFIGS:
        raise ValueError("Unsupported seed/configuration")
    rng = random.Random(seed)
    people = list(range(1000))
    rng.shuffle(people)
    repeats = people[:200] if configuration != "Clean" else []
    dual_order = list(range(1000))
    rng.shuffle(dual_order)
    dual = set(dual_order[:200])
    names = {p: f"SYN-NAME-{p:04}" for p in people}
    contacts = {p: f"SYN-CONTACT-{p:04}" for p in people}
    scenarios = dict.fromkeys(people, "clean")
    if configuration == "Mixed":
        remaining = [p for p in people if p not in set(repeats)]
        rng.shuffle(remaining)
        offset = 0
        for label, count in (("name_collision", 40), ("contact_collision", 40),
                             ("both_collision", 20)):
            selected = remaining[offset:offset+count]
            for a, b in zip(selected[::2], selected[1::2]):
                if label != "contact_collision":
                    names[b] = names[a]
                if label != "name_collision":
                    contacts[b] = contacts[a]
                scenarios[a] = scenarios[b] = label
            offset += count
    variants = {}
    for index, p in enumerate(repeats):
        label = ("normalized_repeat", "typo_repeat", "missing_contact_repeat",
                 "exact_repeat")[index//50] if configuration == "Mixed" else "exact_repeat"
        scenarios[p] = label
        variants[p] = label
    events = []
    for p in range(1000):
        for kind in (("farmer", "processor") if p in dual else ("farmer",)):
            events.append((p, kind, names[p], contacts[p], ()))
        if p in variants:
            name, contact, defects = names[p], contacts[p], ()
            if variants[p] == "normalized_repeat":
                name, contact = f" {name.lower()} ", f" {contact.lower()} "
                defects = ("name_whitespace", "contact_whitespace")
            elif variants[p] == "typo_repeat":
                name += "-TYPO"
            elif variants[p] == "missing_contact_repeat":
                contact, defects = None, ("missing_contact",)
            events.append((p, "farmer", name, contact, defects))
    ids = list(range(len(events)))
    random.Random(f"{seed}:ids").shuffle(ids)
    observations, truth = [], []
    for index, (p, kind, name, contact, defects) in enumerate(events):
        sid = f"SYN-EVENT-{ids[index]:06}"
        observations.append(Observation(sid, name, contact, kind,
                                        ("pending", "accepted", "rejected")[index % 3]))
        truth.append(Truth(sid, f"person-{p}", f"role-{p}-{kind}", scenarios[p], defects))
    random.Random(f"{seed}:rows").shuffle(observations)
    validate(observations, truth)
    return observations, truth


def grouped_pairs(groups: dict) -> set[tuple[str, str]]:
    return {pair for members in groups.values() for pair in combinations(sorted(members), 2)}


def detect(observations: list[Observation], baseline: str) -> dict[str, set]:
    """Observation-only interface: no truth, seed or generation configuration."""
    if baseline not in ("B0", "B1"):
        raise ValueError("Unsupported baseline")
    groups, defects = defaultdict(list), set()
    kinds = {r.submission_id: r.role_kind for r in observations}
    for row in observations:
        for field, token in (("name", row.name_token), ("contact", row.contact_token)):
            if token is None or not token.strip():
                defects.add((row.submission_id, f"missing_{field}"))
            if token is not None and token != token.strip():
                defects.add((row.submission_id, f"{field}_whitespace"))
        tokens = (row.name_token, row.contact_token)
        if any(t is None or not t.strip() for t in tokens):
            continue
        key = tuple(t.strip().casefold() if baseline == "B1" else t for t in tokens)
        groups[key].append(row.submission_id)
    people = grouped_pairs(groups)
    return {"same_person": people,
            "duplicate_role": {(a, b) for a, b in people if kinds[a] == kinds[b]},
            "quality": defects}


def confusion(actual: set, predicted: set, universe: int) -> dict:
    tp, fp, fn = len(actual & predicted), len(predicted-actual), len(actual-predicted)
    tn = universe-tp-fp-fn
    if tn < 0:
        raise ValueError("Invalid evaluation universe")
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "universe": universe,
            "true_pairs_or_labels": len(actual), "predicted_pairs_or_labels": len(predicted),
            "precision": tp/(tp+fp) if tp+fp else None,
            "recall": tp/(tp+fn) if tp+fn else None,
            "false_positive_rate": fp/(fp+tn) if fp+tn else None}


def sql_counts(truth: list[Truth], predictions: dict[str, set]) -> dict[str, tuple[int, int, int]]:
    """Independent truth pair construction and TP/FP/FN joins in SQLite."""
    with sqlite3.connect(":memory:") as db:
        db.executescript("""
        CREATE TABLE truth(id TEXT PRIMARY KEY, person TEXT NOT NULL, role TEXT NOT NULL);
        CREATE TABLE actual(kind TEXT, a TEXT, b TEXT, PRIMARY KEY(kind,a,b));
        CREATE TABLE predicted(kind TEXT, a TEXT, b TEXT, PRIMARY KEY(kind,a,b));
        """)
        db.executemany("INSERT INTO truth VALUES(?,?,?)",
                       [(t.submission_id, t.true_person_id, t.true_role_id) for t in truth])
        for kind, column in (("same_person", "person"), ("duplicate_role", "role")):
            db.execute(f"INSERT INTO actual SELECT ?,a.id,b.id FROM truth a JOIN truth b "
                       f"ON a.{column}=b.{column} AND a.id<b.id", (kind,))
        db.executemany("INSERT INTO actual VALUES('quality',?,?)",
                       [(t.submission_id, rule) for t in truth for rule in t.defect_labels])
        for kind, pairs in predictions.items():
            db.executemany("INSERT INTO predicted VALUES(?,?,?)",
                           [(kind, a, b) for a, b in pairs])
        result = {}
        for kind in predictions:
            tp = db.execute("""SELECT COUNT(*) FROM actual a JOIN predicted p
                USING(kind,a,b) WHERE kind=?""", (kind,)).fetchone()[0]
            actual = db.execute("SELECT COUNT(*) FROM actual WHERE kind=?", (kind,)).fetchone()[0]
            predicted = db.execute("SELECT COUNT(*) FROM predicted WHERE kind=?",
                                   (kind,)).fetchone()[0]
            result[kind] = (tp, predicted-tp, actual-tp)
        for rule in RULES:
            tp = db.execute("""SELECT COUNT(*) FROM actual a JOIN predicted p
                USING(kind,a,b) WHERE kind='quality' AND b=?""", (rule,)).fetchone()[0]
            a = db.execute("SELECT COUNT(*) FROM actual WHERE kind='quality' AND b=?",
                           (rule,)).fetchone()[0]
            p = db.execute("SELECT COUNT(*) FROM predicted WHERE kind='quality' AND b=?",
                           (rule,)).fetchone()[0]
            result[rule] = (tp, p-tp, a-tp)
        return result


def evaluate(observations: list[Observation], truth: list[Truth], baseline: str) -> dict:
    validate(observations, truth)
    predictions = detect(observations, baseline)
    actual = {}
    for relation, attr in (("same_person", "true_person_id"),
                           ("duplicate_role", "true_role_id")):
        groups = defaultdict(list)
        for t in truth:
            groups[getattr(t, attr)].append(t.submission_id)
        actual[relation] = grouped_pairs(groups)
    actual["quality"] = {(t.submission_id, r) for t in truth for r in t.defect_labels}
    n = len(observations)
    metrics = {kind: confusion(actual[kind], predictions[kind], n*len(RULES)
                              if kind == "quality" else n*(n-1)//2) for kind in actual}
    crosscheck = sql_counts(truth, predictions)
    for kind, metric in metrics.items():
        if tuple(metric[k] for k in ("tp", "fp", "fn")) != crosscheck[kind]:
            raise ValueError("SQL/Python reconciliation failed")
    metrics["quality_by_rule"] = {
        rule: confusion({v for v in actual["quality"] if v[1] == rule},
                        {v for v in predictions["quality"] if v[1] == rule}, n)
        for rule in RULES}
    for rule, metric in metrics["quality_by_rule"].items():
        if tuple(metric[k] for k in ("tp", "fp", "fn")) != crosscheck[rule]:
            raise ValueError("Per-rule SQL/Python reconciliation failed")
    scenarios = {}
    for scenario in sorted({t.scenario for t in truth}):
        ids = {t.submission_id for t in truth if t.scenario == scenario}
        k = len(ids)
        scenarios[scenario] = {
            relation: confusion({p for p in actual[relation] if ids.intersection(p)},
                                {p for p in predictions[relation] if ids.intersection(p)},
                                k*(n-k)+k*(k-1)//2)
            for relation in ("same_person", "duplicate_role")}
    return {"metrics": metrics, "scenario_pair_metrics": scenarios,
            "reconciliation": "SQL/Python TP/FP/FN exact; TN derived from shared universe"}


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


def study(seeds: tuple[int, ...]) -> dict:
    runs = []
    for seed in seeds:
        for config in CONFIGS:
            observations, truth = generate(seed, config)
            runs.append({
                "seed": seed, "configuration": config,
                "observation_sha256": digest(sorted([asdict(r) for r in observations],
                                                    key=lambda r: r["submission_id"])),
                "truth_sha256": digest(sorted([asdict(t) for t in truth],
                                              key=lambda t: t["submission_id"])),
                "events": len(observations),
                "people": len({t.true_person_id for t in truth}),
                "intended_roles": len({t.true_role_id for t in truth}),
                "scenario_event_counts": {s: sum(t.scenario == s for t in truth)
                                          for s in sorted({t.scenario for t in truth})},
                "baselines": {b: evaluate(observations, truth, b) for b in ("B0", "B1")},
            })
    return {"source": "SYNTHETIC DEMONSTRATION DATA", "contract_version": "1.0",
            "generator_version": "1.0", "protocol": "M3_04_PROTOCOL.md v1.0",
            "protocol_sha256": hashlib.sha256(
                Path("docs/experiments/M3_04_PROTOCOL.md").read_bytes()).hexdigest(),
            "python": sys.version.split()[0], "sqlite": sqlite3.sqlite_version,
            "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "lock_sha256": hashlib.sha256(Path("requirements/e1.lock").read_bytes()).hexdigest(),
            "runs": runs}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("development", "evaluation"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.output.resolve().is_relative_to(Path.cwd().resolve()/"reports/private"):
        raise ValueError("Output must be inside reports/private")
    result = study(DEVELOPMENT_SEEDS if args.phase == "development" else EVALUATION_SEEDS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print("Synthetic aggregate evaluation saved under ignored reports/private")


if __name__ == "__main__":
    main()
