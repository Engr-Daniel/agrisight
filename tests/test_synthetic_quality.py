"""Manually checked synthetic identity, role and defect examples; no survey input."""

from dataclasses import replace

import pytest

from agrisight.synthetic_quality import (
    Observation,
    Truth,
    confusion,
    detect,
    evaluate,
    generate,
    validate,
)


def example():
    observations = [
        Observation("a", "SYN-A", "SYN-C", "farmer", "pending"),
        Observation("b", "SYN-A", "SYN-C", "processor", "accepted"),
        Observation("c", "SYN-A", "SYN-C", "farmer", "rejected"),
        Observation("d", "SYN-A", "SYN-C", "farmer", "accepted"),
    ]
    truth = [Truth("a", "p1", "r1", "repeat"), Truth("b", "p1", "r2", "repeat"),
             Truth("c", "p1", "r1", "repeat"), Truth("d", "p2", "r3", "collision")]
    return observations, truth


def test_manual_dual_role_repeat_and_collision():
    observations, truth = example()
    result = evaluate(observations, truth, "B0")["metrics"]
    assert (result["same_person"]["tp"], result["same_person"]["fp"],
            result["same_person"]["fn"], result["same_person"]["tn"]) == (3, 3, 0, 0)
    assert result["same_person"]["precision"] == 0.5
    assert (result["duplicate_role"]["tp"], result["duplicate_role"]["fp"],
            result["duplicate_role"]["fn"], result["duplicate_role"]["tn"]) == (1, 2, 0, 3)
    assert ("a", "b") not in detect(observations, "B0")["duplicate_role"]


def test_three_repeat_events_make_three_pairs():
    observations = [Observation(s, "SYN-A", "SYN-C", "farmer", "pending") for s in "abc"]
    truth = [Truth(s, "p", "r", "repeat") for s in "abc"]
    assert evaluate(observations, truth, "B0")["metrics"]["duplicate_role"]["tp"] == 3


@pytest.mark.parametrize("name,contact,raw,normalized", [
    (" syn-a ", " syn-c ", False, True),
    ("SYN-A-TYPO", "SYN-C", False, False),
    ("SYN-A", None, False, False),
    ("SYN-A", "SYN-OTHER", False, False),
    ("SYN-OTHER", "SYN-C", False, False),
])
def test_normalization_and_missed_pairs(name, contact, raw, normalized):
    observations = [Observation("a", "SYN-A", "SYN-C", "farmer", "pending"),
                    Observation("b", name, contact, "farmer", "accepted")]
    assert bool(detect(observations, "B0")["same_person"]) is raw
    assert bool(detect(observations, "B1")["same_person"]) is normalized


def test_whitespace_null_and_defect_known_truth():
    observations = [Observation("a", " ", None, "farmer", "accepted"),
                    Observation("b", None, " SYN-C ", "processor", "pending")]
    truth = [Truth("a", "p1", "r1", "missing",
                   ("missing_name", "missing_contact", "name_whitespace")),
             Truth("b", "p2", "r2", "missing", ("missing_name", "contact_whitespace"))]
    result = evaluate(observations, truth, "B1")["metrics"]
    assert result["quality"]["tp"] == 5
    assert result["quality"]["tn"] == 3
    assert result["quality"]["fp"] == result["quality"]["fn"] == 0
    assert result["same_person"]["predicted_pairs_or_labels"] == 0
    assert result["quality_by_rule"]["missing_name"]["tp"] == 2


def test_empty_and_undefined_rates():
    result = evaluate([], [], "B0")["metrics"]
    assert result["quality"]["universe"] == 0
    assert result["same_person"]["precision"] is None
    assert result["same_person"]["recall"] is None
    assert result["same_person"]["false_positive_rate"] is None
    assert confusion({("a", "b")}, set(), 1)["recall"] == 0


def test_row_order_and_truth_labels_do_not_change_predictions():
    observations, truth = example()
    before = detect(observations, "B1")
    assert before == detect(list(reversed(observations)), "B1")
    assert evaluate(observations, truth, "B1") == evaluate(
        list(reversed(observations)), list(reversed(truth)), "B1")


@pytest.mark.parametrize("mutation", ["duplicate", "missing_id", "type", "role", "status",
                                     "missing_truth", "duplicate_truth", "owner", "labels",
                                     "person_kind"])
def test_contract_failures(mutation):
    observations, truth = example()
    if mutation == "duplicate":
        observations[1] = replace(observations[1], submission_id="a")
    elif mutation == "missing_id":
        observations[1] = replace(observations[1], submission_id=" ")
    elif mutation == "type":
        observations[1] = replace(observations[1], name_token=42)
    elif mutation == "role":
        observations[1] = replace(observations[1], role_kind="unknown")
    elif mutation == "status":
        observations[1] = replace(observations[1], status="unknown")
    elif mutation == "missing_truth":
        truth.pop()
    elif mutation == "duplicate_truth":
        truth.append(truth[0])
    elif mutation == "owner":
        truth[2] = replace(truth[2], true_person_id="other")
    elif mutation == "labels":
        truth[2] = replace(truth[2], defect_labels=("unknown",))
    else:
        truth[2] = replace(truth[2], true_role_id="another-role")
    with pytest.raises(ValueError):
        evaluate(observations, truth, "B0")


@pytest.mark.parametrize("configuration,events", [("Clean", 1200), ("Exact-repeat", 1400),
                                                 ("Mixed", 1400)])
def test_generator_invariants_and_determinism(configuration, events):
    observations, truth = generate(101, configuration)
    assert (observations, truth) == generate(101, configuration)
    assert len(observations) == events
    assert len({t.true_person_id for t in truth}) == 1000
    assert len({t.true_role_id for t in truth}) == 1200
    validate(observations, truth)
    for baseline in ("B0", "B1"):
        evaluate(observations, truth, baseline)
    if configuration == "Mixed":
        assert sum("missing_contact" in t.defect_labels for t in truth) == 50
        assert sum("name_whitespace" in t.defect_labels for t in truth) == 50
        assert len({t.true_person_id for t in truth if t.scenario == "both_collision"}) == 20


def test_evaluation_detects_mislabelling_as_errors():
    observations, truth = example()
    truth = [replace(t, defect_labels=("missing_name",)) if t.submission_id == "a" else t
             for t in truth]
    assert evaluate(observations, truth, "B0")["metrics"]["quality"]["fn"] == 1


def test_unknown_configuration_and_baseline_fail():
    with pytest.raises(ValueError):
        generate(101, "unknown")
    with pytest.raises(ValueError):
        detect([], "unknown")


def test_independent_disagreement_aborts(monkeypatch):
    import agrisight.synthetic_quality as module

    original = module.sql_counts

    def incorrect(truth, predictions):
        result = original(truth, predictions)
        result["same_person"] = (999, 0, 0)
        return result

    monkeypatch.setattr(module, "sql_counts", incorrect)
    with pytest.raises(ValueError, match="reconciliation"):
        evaluate(*example(), "B0")


def test_cli_refuses_output_outside_private(monkeypatch, tmp_path):
    import sys

    from agrisight.synthetic_quality import main

    output = tmp_path / "outside.json"
    monkeypatch.setattr(sys, "argv", ["synthetic_quality", "--phase", "development",
                                     "--output", str(output)])
    with pytest.raises(ValueError, match="reports/private"):
        main()
    assert not output.exists()


def test_study_records_exact_policy_and_input_bytes(tmp_path, monkeypatch):
    import hashlib
    from pathlib import Path

    import agrisight.synthetic_quality as module

    monkeypatch.chdir(tmp_path)
    protocol = tmp_path/"docs/experiments/M3_04_PROTOCOL.md"
    protocol.parent.mkdir(parents=True)
    protocol.write_bytes(b"policy fixture\n")
    lock = tmp_path/"requirements/e1.lock"
    lock.parent.mkdir()
    lock.write_bytes(b"frozen lock\r\n")
    result = module.study(())
    assert result["provenance_policy"] == "agrisight-text-lf-v1"
    assert result["protocol_sha256"] == hashlib.sha256(protocol.read_bytes()).hexdigest()
    assert result["lock_sha256"] == hashlib.sha256(lock.read_bytes()).hexdigest()
    assert result["code_sha256"] == hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
    # Raw-byte provenance must distinguish CRLF from LF, never silently normalize.
    protocol.write_bytes(b"policy fixture\r\n")
    assert module.study(())["protocol_sha256"] != result["protocol_sha256"]
