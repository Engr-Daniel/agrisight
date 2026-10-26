"""Independent Python/SQL KPI checks on a tiny SYNTHETIC fixture."""
import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    role_id: str
    person_id: str
    kind: str
    status: str
    complete: bool

ROLES = [
    Role("r1", "p1", "farmer", "accepted", True),
    Role("r2", "p2", "farmer", "accepted", True),
    Role("r3", "p2", "processor", "accepted", True),
    Role("r4", "p3", "farmer", "pending", False),
    Role("r5", "p4", "processor", "accepted", False),
    Role("r6", "p5", "farmer", "rejected", False),
]
FIELDS = ("submitted", "accepted", "farmers", "processors", "people", "complete", "incomplete")

def python_metrics(roles=ROLES):
    accepted = [r for r in roles if r.status == "accepted"]
    return dict(zip(FIELDS, (
        len(roles), len(accepted),
        sum(r.kind == "farmer" for r in accepted),
        sum(r.kind == "processor" for r in accepted),
        len({r.person_id for r in accepted}),
        sum(r.complete for r in accepted),
        sum(not r.complete for r in accepted),
    )))

SQL = """
SELECT COUNT(*),
 COALESCE(SUM(CASE WHEN status='accepted' THEN 1 ELSE 0 END),0),
 COALESCE(SUM(CASE WHEN status='accepted' AND kind='farmer' THEN 1 ELSE 0 END),0),
 COALESCE(SUM(CASE WHEN status='accepted' AND kind='processor' THEN 1 ELSE 0 END),0),
 COUNT(DISTINCT CASE WHEN status='accepted' THEN person_id END),
 COALESCE(SUM(CASE WHEN status='accepted' AND complete=1 THEN 1 ELSE 0 END),0),
 COALESCE(SUM(CASE WHEN status='accepted' AND complete=0 THEN 1 ELSE 0 END),0)
FROM actor_roles
"""

def sql_metrics(roles=ROLES):
    with sqlite3.connect(":memory:") as db:
        db.execute("""CREATE TABLE actor_roles(
          role_id TEXT PRIMARY KEY,
          person_id TEXT NOT NULL,
          kind TEXT NOT NULL CHECK(kind IN ('farmer','processor')),
          status TEXT NOT NULL CHECK(status IN ('accepted','pending','rejected')),
          complete INTEGER NOT NULL CHECK(complete IN (0,1))
        )""")
        db.executemany("INSERT INTO actor_roles VALUES(?,?,?,?,?)", [
            (r.role_id,r.person_id,r.kind,r.status,int(r.complete)) for r in roles
        ])
        return dict(zip(FIELDS, db.execute(SQL).fetchone()))

def main():
    import json
    p, s = python_metrics(), sql_metrics()
    assert p == s, (p, s)
    print(json.dumps({"source":"SYNTHETIC DEMONSTRATION","metrics":p},indent=2))

if __name__ == "__main__":
    main()
