#!/usr/bin/env python3
"""QA/QC checks for the data dictionary.

Rules checked:
  DD-01  Globally_unique_identifier values in PROPERTIES.csv must be unique.
  DD-02  Property_key values must match ^urn:demo:property:[a-z0-9_]+$

Usage:
    python scripts/qaqc/run_checks.py

Writes: outputs/qaqc_results.txt
"""

import csv
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROPERTIES_CSV = REPO_ROOT / "data_dictionary" / "PROPERTIES_23386.csv"
OUTPUT_FILE = REPO_ROOT / "outputs" / "qaqc_results.txt"

PROPERTY_KEY_RE = re.compile(r"^urn:demo:property:[a-z0-9_]+$")


def load_properties():
    with open(PROPERTIES_CSV, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def check_dd01(rows):
    """DD-01: Globally_unique_identifier must be unique across all rows."""
    violations = []
    seen = {}
    for i, row in enumerate(rows, start=2):  # row 1 is the header
        guid = row.get("Globally_unique_identifier", "").strip()
        if not guid:
            violations.append(f"  Row {i}: GUID is blank (property: {row.get('Property_key', '?')})")
        elif guid in seen:
            violations.append(
                f"  Row {i}: duplicate GUID {guid!r} "
                f"(also on row {seen[guid]}, property: {row.get('Property_key', '?')})"
            )
        else:
            seen[guid] = i
    return violations


def check_dd02(rows):
    """DD-02: Property_key must match ^urn:demo:property:[a-z0-9_]+$"""
    violations = []
    for i, row in enumerate(rows, start=2):
        key = row.get("Property_key", "").strip()
        if not PROPERTY_KEY_RE.match(key):
            violations.append(f"  Row {i}: invalid Property_key {key!r}")
    return violations


def main():
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    rows = load_properties()
    total = len(rows)

    dd01 = check_dd01(rows)
    dd02 = check_dd02(rows)

    lines = []
    lines.append("QA/QC Results — Data Dictionary")
    lines.append(f"File:  {PROPERTIES_CSV.relative_to(REPO_ROOT)}")
    lines.append(f"Rows checked: {total}")
    lines.append("")

    for rule_id, label, violations in [
        ("DD-01", "GUID uniqueness", dd01),
        ("DD-02", "Property key format", dd02),
    ]:
        if violations:
            lines.append(f"[FAIL] {rule_id}: {label} — {len(violations)} violation(s)")
            lines.extend(violations)
        else:
            lines.append(f"[PASS] {rule_id}: {label}")
        lines.append("")

    all_passed = not dd01 and not dd02
    lines.append("Overall: ALL CHECKS PASSED" if all_passed else "Overall: VIOLATIONS FOUND — review above")

    report = "\n".join(lines)
    OUTPUT_FILE.write_text(report + "\n", encoding="utf-8")

    print(report)
    print(f"\nResults written to {OUTPUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
