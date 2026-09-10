"""Enumerate a declared finite fault domain; no model calls or timing claims."""
import csv
import json
import platform
from dataclasses import replace
from pathlib import Path
from ir_contract import Registry, Rejected, digest, fixture

FAULTS = [
    ("source_digest", "wrong"), ("theme_version", "theme-v0"),
    ("principal", "outsider"), ("domain", "public"),
    ("period", "2025Q2"), ("unit", "EUR"),
    ("rationale_id", "unapproved"), ("relation", "customer-id"),
    ("operation", "write"), ("max_bytes", 1),
]


def main():
    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    records = []
    for mask in range(1 << len(FAULTS)):
        s, c = fixture()
        faults = {key: value for i, (key, value) in enumerate(FAULTS) if mask & (1 << i)}
        c = replace(c, **faults)
        registry = Registry(s)
        try:
            result = registry.execute(registry.prepare(c, 10), 10)
            accepted, code = True, "OK"
            assert result["digest"] == digest(s.content)
        except Rejected as exc:
            accepted, code = False, exc.code
        # Independent finite-domain oracle: the fixture is valid; each injected
        # mutation violates a stated requirement. No call to Registry.check.
        expected = mask == 0
        records.append({"mask": mask, "faults": ";".join(faults),
                        "accepted": int(accepted), "expected": int(expected),
                        "agrees": int(accepted == expected), "code": code})
    with (out / "fault-cases.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    summary = {"study": "finite synthetic contract conformance",
               "python": platform.python_version(), "fault_dimensions": len(FAULTS),
               "cases": len(records), "accepted": sum(r["accepted"] for r in records),
               "rejected": sum(not r["accepted"] for r in records),
               "oracle_disagreements": sum(not r["agrees"] for r in records),
               "runtime_scaling_measured": False, "P1_verdict": "not evaluated",
               "limitations": ["single trusted in-process registry", "one source fixture",
                               "no LLM, distributed service, retrieval or adversarial evaluation",
                               "finite enumeration is not an estimate of production failure probability"],
               "sha256": {p.name: digest(p.read_bytes()) for p in
                           [Path(__file__), Path(__file__).with_name("ir_contract.py")]}}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    assert not summary["oracle_disagreements"]


if __name__ == "__main__":
    main()
