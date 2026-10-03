"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return the systolic reading from every usable encounter."""
    return [systolic for _, _, systolic in encounters]


def mean_systolic(readings):
    """Return the mean systolic reading, or None for an empty list."""
    return sum(readings) / len(readings) if readings else None


def count_patients(encounters):
    """Count distinct patient IDs among usable encounters."""
    return len({patient_id for patient_id, _, _ in encounters})


def patients_at_or_above(encounters, cutoff):
    """Return distinct IDs with at least one reading at or above cutoff."""
    return {patient_id for patient_id, _, systolic in encounters if systolic >= cutoff}
