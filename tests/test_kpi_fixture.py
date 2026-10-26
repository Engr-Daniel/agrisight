"""Tests for person/role grain and verified numerical results."""
import sqlite3
import pytest
from agrisight.kpi_fixture import ROLES, Role, python_metrics, sql_metrics

EXPECTED = dict(submitted=6,accepted=4,farmers=2,processors=2,people=3,
                complete=3,incomplete=1)

def test_fixture_ground_truth():
    assert python_metrics() == EXPECTED

def test_independent_sql_agrees():
    assert sql_metrics() == python_metrics() == EXPECTED

def test_role_count_not_person_count():
    assert python_metrics()["accepted"] == 4
    assert python_metrics()["people"] == 3

def test_status_exclusion():
    assert python_metrics()["submitted"] - python_metrics()["accepted"] == 2

def test_incomplete_accepted_is_counted():
    assert sql_metrics()["incomplete"] == 1

def test_empty_input():
    assert python_metrics([]) == sql_metrics([])

@pytest.mark.parametrize("field,value", [("kind","unknown"),("status","invalid")])
def test_invalid_values_rejected(field,value):
    from dataclasses import replace
    with pytest.raises(sqlite3.IntegrityError):
        sql_metrics([replace(ROLES[0], **{field:value})])

def test_duplicate_role_key_rejected():
    with pytest.raises(sqlite3.IntegrityError):
        sql_metrics([ROLES[0], Role("r1","p9","farmer","accepted",True)])
