import json, sys
from collections import Counter
from validate import validate
from report_model import ReportModel, calibrate
from prob import chi_square

CHI2_CRIT_001 = {4: 18.467, 2: 13.816}   # chi-square critical value at p = 0.001, df = 4 (five materials)

def load(path):
    with open(path) as f:
        return [json.loads(l) for l in f]

def classify(report, model, threshold):
    """Gate 1: schema + logic (Lab 4). Gate 2: statistical plausibility.
    Returns (verdict, detail) where verdict is accept / quarantine / reject."""
    ok, reasons, _ = validate(report)
    if not ok:
        return "reject", reasons
    # TODO: compute the report's log-likelihood under `model`.
    #       If it is below `threshold`, return ("quarantine", [message]) where
    #       message looks like  "improbable: log-likelihood -7.43 < threshold -6.56"
    #       (two decimal places; the word "improbable" must appear).
    #       Otherwise return ("accept", []).
    log_likelihood = model.log_likelihood(report)
    if log_likelihood < threshold:
        message = f"improbable: log-likelihood {log_likelihood:.2f} < threshold {threshold:.2f}"
        return "quarantine", [message]
    return "accept", []

def batch_drift(reports, model):
    """Batch-level check. Returns {check_name: (statistic, critical_value, drifted)}."""
    mat = Counter(r["material"] for r in reports)
    s = chi_square(mat, model.p_material)
    severity_counts = Counter(r["severity"] for r in reports)
    severity_stat = chi_square(severity_counts, model.p_severity_mix)
    return {
        "material_mix": (round(s, 2), CHI2_CRIT_001[4], s > CHI2_CRIT_001[4]),
        "severity_mix": (
            round(severity_stat, 2),
            CHI2_CRIT_001[2],
            severity_stat > CHI2_CRIT_001[2],
        ),
    }

def run(batch_path, reference_path="data/reference.jsonl", q=0.02):
    ref = load(reference_path)
    model = ReportModel(ref)
    threshold = calibrate(model, ref, q)
    verdicts, passed, summary = {}, [], Counter()
    for r in load(batch_path):
        v, detail = classify(r, model, threshold)
        verdicts[r.get("id")] = (v, detail)
        summary[v] += 1
        if v != "reject":
            passed.append(r)
    return {"summary": dict(summary), "drift": batch_drift(passed, model),
            "verdicts": verdicts, "threshold": round(threshold, 2)}

def main(batch_path, log_path=None):
    res = run(batch_path)
    log_path = log_path or batch_path.replace(".jsonl", ".quality.log.jsonl")
    with open(log_path, "w") as log:
        for rid, (verdict, detail) in res["verdicts"].items():
            if verdict != "accept":
                log.write(json.dumps({"id": rid, "verdict": verdict, "detail": detail}) + "\n")
    print(json.dumps({k: res[k] for k in ("summary", "drift", "threshold")}))

if __name__ == "__main__":
    main(*sys.argv[1:])
