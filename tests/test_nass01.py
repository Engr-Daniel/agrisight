"""Known-truth NASS-01 contracts; real files are never required in CI."""

import hashlib
import io
import json
import sqlite3
import zipfile

import pytest

pd = pytest.importorskip("pandas")

from agrisight import nass01


def frame(codes):
    return pd.DataFrame({"hhid": list(range(1, len(codes) + 1)), "s00_q15a": codes})


def test_known_truth_with_exclusions_and_no_source_mutation():
    data = frame([1, 2, 1, None, 9])
    before = data.copy(deep=True)
    result = nass01.calculate(data)["counts_and_rates"]
    assert result == {
        "input_rows": 5, "numerator": 2, "denominator": 3, "no_count": 1,
        "missing_count": 1, "invalid_count": 1, "excluded_count": 2,
        "proportion": 2 / 3, "percentage": 200 / 3,
    }
    pd.testing.assert_frame_equal(data, before)


@pytest.mark.parametrize("codes", [[], [None, 9], [pd.io.stata.StataMissingValue(102)]])
def test_zero_eligible_responses_are_undefined(codes):
    result = nass01.calculate(frame(codes))["counts_and_rates"]
    assert result["denominator"] == 0
    assert result["proportion"] is None
    assert result["percentage"] is None


@pytest.mark.parametrize("keys", [[1, 1.0], [1, None], [1, " "]])
def test_ambiguous_keys_fail_instead_of_deduplicating(keys):
    data = frame([1, 2])
    data["hhid"] = keys
    with pytest.raises(ValueError, match="household key"):
        nass01.calculate(data)


@pytest.mark.parametrize("code", [True, "1"])
def test_wrong_code_types_are_not_coerced(code):
    with pytest.raises(TypeError, match="numeric"):
        nass01.calculate(frame([code]))


def test_missing_schema_and_period_fail():
    with pytest.raises(ValueError, match="Required columns"):
        nass01.calculate(pd.DataFrame({"hhid": [1]}))
    with pytest.raises(ValueError, match="period"):
        nass01.check_period(pd.DataFrame({"mainAgSeason": ["different"]}))


def test_row_order_invariance_and_float_division():
    data = frame([1, 2])
    assert nass01.calculate(data) == nass01.calculate(data.iloc[::-1])
    assert nass01.calculate(data)["counts_and_rates"]["proportion"] == 0.5


def test_sql_constraints_and_null_retention():
    with sqlite3.connect(":memory:") as db:
        db.executescript(nass01.sql_model())
        db.execute("INSERT INTO stg_nass_households VALUES('A',NULL)")
        assert db.execute("SELECT response_status FROM int_nass01_eligibility").fetchone() == (
            "missing",
        )
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("INSERT INTO stg_nass_households VALUES('A',1)")
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("INSERT INTO stg_nass_households VALUES(NULL,1)")


def test_reconciliation_mismatch_fails():
    result = nass01.python_indicator(frame([1]))
    wrong = dict(result, numerator=0)
    with pytest.raises(ValueError, match="Integer reconciliation"):
        nass01.reconcile(result, wrong)
    with pytest.raises(ValueError, match="Rate reconciliation"):
        nass01.reconcile(result, dict(result, proportion=0.5))


def test_output_and_archive_guards(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    archive = tmp_path / "bad.zip"
    archive.write_bytes(b"not a source file")
    with pytest.raises(ValueError, match="reports/private"):
        nass01.run(archive, tmp_path / "public.json")
    with pytest.raises(ValueError, match="Archive hash"):
        nass01.run(archive, tmp_path / "reports/private/test.json")


def test_complete_stata_to_private_indicator(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data = frame([1, 2, 1])
    data["mainAgSeason"] = nass01.EXPECTED_PERIOD
    data["referenceAgYear"] = nass01.EXPECTED_YEAR
    stata = io.BytesIO()
    data.to_stata(stata, write_index=False, version=114)
    archive = tmp_path / "synthetic.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("1_households.dta", stata.getvalue())
    monkeypatch.setattr(nass01, "ARCHIVE_SHA256", hashlib.sha256(archive.read_bytes()).hexdigest())
    (tmp_path / "requirements").mkdir()
    (tmp_path / "requirements/e1.lock").write_text("# synthetic test lock\n")
    output = tmp_path / "reports/private/indicator.json"
    nass01.run(archive, output)
    result = json.loads(output.read_text())
    assert result["counts_and_rates"]["numerator"] == 2
    assert result["counts_and_rates"]["denominator"] == 3
    assert "hhid" not in result
    assert result["definition"]["weighting"] == "unweighted"
