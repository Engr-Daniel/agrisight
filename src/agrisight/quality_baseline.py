"""M0-05: dependency-free validation baseline on synthetic registration records.

This demonstrates contract behavior, not an integration of Pandera or GX Core.
"""
from dataclasses import dataclass

ALLOWED_ROLES = frozenset({"farmer", "processor"})
ALLOWED_STATUSES = frozenset({"accepted", "pending", "rejected"})


@dataclass(frozen=True)
class QualityIssue:
    row: int
    field: str
    code: str


def validate_roles(rows: list[dict]) -> list[QualityIssue]:
    """Report field and row issues without dropping or changing raw submissions."""
    issues: list[QualityIssue] = []
    seen_ids: set[str] = set()
    required = ("role_id", "person_id", "kind", "status")

    for index, record in enumerate(rows):
        for field in required:
            if field not in record or not isinstance(record[field], str) or not record[field].strip():
                issues.append(QualityIssue(index, field, "missing_required"))

        role_id = record.get("role_id")
        if isinstance(role_id, str) and role_id.strip():
            if role_id in seen_ids:
                issues.append(QualityIssue(index, "role_id", "duplicate_role_id"))
            seen_ids.add(role_id)

        if "kind" in record and record["kind"] not in ALLOWED_ROLES:
            issues.append(QualityIssue(index, "kind", "invalid_category"))
        if "status" in record and record["status"] not in ALLOWED_STATUSES:
            issues.append(QualityIssue(index, "status", "invalid_category"))

        if "complete" not in record or type(record["complete"]) is not bool:
            issues.append(QualityIssue(index, "complete", "invalid_boolean"))

    return issues


def example_inputs() -> tuple[list[dict], list[dict]]:
    valid = [
        {"role_id": "R1", "person_id": "P1", "kind": "farmer", "status": "accepted", "complete": True},
        {"role_id": "R2", "person_id": "P1", "kind": "processor", "status": "accepted", "complete": False},
    ]
    invalid = [
        valid[0].copy(),
        {"role_id": "R1", "person_id": "", "kind": "dealer", "status": "unknown", "complete": 1},
    ]
    return valid, invalid


if __name__ == "__main__":
    good, bad = example_inputs()
    print("Valid fixture findings:", validate_roles(good))
    print("Invalid fixture findings:", validate_roles(bad))
