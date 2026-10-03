#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Return usable (patient ID, visit date, systolic) tuples and skipped count."""
    encounters = []
    skipped = 0
    with data_path.open(encoding="utf-8") as data_file:
        next(data_file)  # Header
        for line_number, line in enumerate(data_file, start=2):
            fields = line.strip().split(",")
            if len(fields) != 3:
                print(f"Skipping row {line_number}: expected three fields.")
                skipped += 1
                continue
            try:
                systolic = int(fields[2])
            except ValueError:
                print(f"Skipping row {line_number}: invalid systolic reading.")
                skipped += 1
                continue
            if not 60 <= systolic <= 250:
                print(f"Skipping row {line_number}: reading outside 60-250 mmHg.")
                skipped += 1
                continue
            encounters.append((fields[0], fields[1], systolic))
    return encounters, skipped


def main():
    """Write a vitals summary and a list of patients needing follow-up."""
    encounters, skipped = read_encounters(DATA_PATH)
    readings = systolic_readings(encounters)
    OUTPUT_DIR.mkdir(exist_ok=True)

    report_path = OUTPUT_DIR / "vitals_report.txt"
    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(report_path.read_text(encoding="utf-8"), end="")

    cutoff = 140
    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        "Reason: A 140 mmHg cutoff prioritizes patients with elevated systolic readings for this week's limited callback capacity.",
        *sorted(patients_at_or_above(encounters, cutoff)),
    ]
    (OUTPUT_DIR / "followup_list.txt").write_text(
        "\n".join(followup_lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
