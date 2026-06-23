import re
from typing import Tuple, Optional


def is_valid_time_format(metric: str) -> Tuple[bool, Optional[int]]:
    if not metric or not isinstance(metric, str):
        return False, None

    s = metric.strip()
    if not s:
        return False, None

    pattern = r"^(?:(?:\d+:\d{2}(?:\.\d{2})?)|(?:\d+(?:\.\d{1,2})?))$"
    if not re.match(pattern, s):
        return False, None

    # Parse to total seconds
    try:
        if ":" in s:
            parts = s.split(":")
            minutes = int(parts[0])
            sec_part = parts[1]

            if "." in sec_part:
                sec, hund = sec_part.split(".")
                total_seconds = minutes * 60 + int(sec) + int(hund) / 100.0
            else:
                total_seconds = minutes * 60 + int(sec_part)
        else:
            total_seconds = float(s)
    except (ValueError, IndexError):
        return False, None

    # Must be a multiple of one tick (0.6 seconds)
    if abs(total_seconds % 0.6) > 1e-6:
        return False, None

    if total_seconds <= 0 or total_seconds > 36000:  # ~10 hours max
        return False, None

    # Convert to ticks
    ticks = int(round(total_seconds / 0.6))  # round for safety

    return True, ticks


test_cases = {
    "0:06": True,
    "0:06.00": True,
    "35:21": True,
    "1:23.45": False,
    "6.0": True,
    "1.80": True,
    "1.90": False,
    ":5": False,
    "2.40": True,
    "": False,
    "0:00": False,
    "10:59.99": False,
    "123:45": True,
    "1.0": False,
    "1.2": True,
}

for k, v in test_cases.items():
    result, _ = is_valid_time_format(k)
    if result == v:
        print(f"Pass: {k:>12} -> {result}")
    else:
        print(f"FAILED.{k:>12}")
