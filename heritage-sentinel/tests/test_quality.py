import hashlib, json, os, subprocess, sys, tempfile
import pytest
import make_data
from quality import load, classify, run, batch_drift
from report_model import ReportModel, calibrate
from validate import validate

REF = load("data/reference.jsonl")
MODEL = ReportModel(REF)
THRESHOLD = calibrate(MODEL, REF, 0.02)

def by_id(path):
    return {r["id"]: r for r in load(path)}

A = by_id("data/incoming_a.jsonl")

def test_reference_data_passes_the_logic_gate():
    # Your "trusted" data must itself obey the Lab 4 rules.
    assert all(validate(r)[0] for r in REF)

def test_calibration_flags_about_two_percent_of_reference():
    flagged = sum(MODEL.log_likelihood(r) < THRESHOLD for r in REF)
    assert 7 <= flagged <= 9          # 2% of 400 = 8, allow +/-1 for percentile conventions

@pytest.mark.parametrize("rid", ["a-odd1", "a-odd2", "a-odd3"])
def test_logic_valid_but_improbable_is_quarantined(rid):
    assert validate(A[rid])[0]                       # Lab 4 alone would accept it
    verdict, detail = classify(A[rid], MODEL, THRESHOLD)
    assert verdict == "quarantine" and "improbable" in detail[0]

@pytest.mark.parametrize("rid", ["a-bad1", "a-bad2"])
def test_impossible_is_rejected_not_quarantined(rid):
    verdict, _ = classify(A[rid], MODEL, THRESHOLD)
    assert verdict == "reject"

def test_unseen_combination_scores_finite():
    ll = MODEL.log_likelihood(A["a-odd1"])           # stone + corrosion never occurs in reference
    assert ll == ll and ll > -100                    # not NaN, not -inf

def test_without_smoothing_unseen_combination_blows_up():
    # TODO: build a model with alpha=0.0 and show that scoring a-odd1
    # (stone + corrosion) raises ValueError. This is the failure that
    # smoothing exists to prevent.
    unsmoothed_model = ReportModel(REF, alpha=0.0)
    with pytest.raises(ValueError):
        unsmoothed_model.log_likelihood(A["a-odd1"])

def test_batch_a_summary():
    res = run("data/incoming_a.jsonl")
    assert res["summary"] == {"accept": 100, "quarantine": 3, "reject": 2}
    assert res["drift"]["material_mix"][2] is False

def test_drifted_batch_passes_every_record_check_but_fails_the_batch_check():
    # TODO: this is the centerpiece. Run the pipeline on incoming_b.jsonl and
    # assert BOTH (1) all 100 reports are individually accepted, and
    # (2) the batch-level drift check fires. Then explain in NOTES.md why no
    # record-level check could ever have caught this.
    res = run("data/incoming_b.jsonl")
    assert res["summary"] == {"accept": 100}
    assert res["drift"]["material_mix"][2] is True

def test_heldout_quarantine_rate_is_near_target():
    # TODO: generate 20 fresh batches of 100 with
    # make_data.make_batch(seed, 100, "h", make_data.MATERIAL_P) for seeds
    # 100..119, score every report, and compute the fraction below THRESHOLD.
    # Assert it falls between 0.5% and 4% (a band, not an exact number: why?).
    reports = [
        report
        for seed in range(100, 120)
        for report in make_data.make_batch(seed, 100, "h", make_data.MATERIAL_P)
    ]
    flagged = sum(MODEL.log_likelihood(report) < THRESHOLD for report in reports)
    rate = flagged / len(reports)
    # Fresh samples vary, so allow a range around the 2% calibration target.
    assert 0.005 <= rate <= 0.04

def test_clean_batches_rarely_raise_drift_alarms():
    alarms = sum(
        batch_drift(make_data.make_batch(s, 100, "c", make_data.MATERIAL_P), MODEL)["material_mix"][2]
        for s in range(100, 150))
    assert alarms <= 1

def test_severity_only_drift_is_detected():
    reports = make_data.make_batch(2, 100, "s", make_data.MATERIAL_P)
    for report in reports:
        if report["severity"] == "minor":
            report["severity"] = "major"
    checks = batch_drift(reports, MODEL)
    assert checks["severity_mix"][2] is True
    assert checks["material_mix"][2] is False


def test_clean_batch_has_no_severity_drift():
    reports = make_data.make_batch(2, 100, "s", make_data.MATERIAL_P)
    checks = batch_drift(reports, MODEL)
    assert checks["severity_mix"][2] is False


def test_data_generation_is_deterministic():
    # TODO: run tools/make_data.py twice, each time into a fresh temporary
    # directory (tempfile.TemporaryDirectory), and assert the two directories
    # contain byte-identical files (compare hashlib.sha256 digests).
    digests = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as output_dir:
            subprocess.run(
                [sys.executable, make_data.__file__, output_dir],
                capture_output=True, text=True, check=True,
            )
            filenames = sorted(os.listdir(output_dir))
            assert filenames == ["incoming_a.jsonl", "incoming_b.jsonl", "reference.jsonl"]
            file_digests = {}
            for filename in filenames:
                with open(os.path.join(output_dir, filename), "rb") as f:
                    file_digests[filename] = hashlib.sha256(f.read()).hexdigest()
            digests.append(file_digests)
    assert digests[0] == digests[1]

def test_pipeline_output_is_reproducible_across_processes():
    runs = [subprocess.run([sys.executable, "scr/quality.py", "data/incoming_a.jsonl",
                            os.devnull], capture_output=True, text=True, check=True).stdout
            for _ in range(2)]
    assert runs[0] == runs[1]
