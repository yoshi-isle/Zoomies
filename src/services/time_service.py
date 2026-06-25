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

    if total_seconds <= 0 or total_seconds > 21600:
        return False, None

    ticks = int(round(total_seconds / 0.6))
    return True, ticks


test_cases = {
    "0:06": True,
    "0:06.00": True,
    "35:21": True,
    "6.0": True,
    "1.80": True,
    "1.90": True,
    ":5": False,
    "2.40": True,
    "": False,
    "0:00": False,
    "123:45": True,
    "1.0": True,
    "1.2": True,
    "adfgiobsrgdjf": False,
    "1:2": False,
    "10-2033420": False,
    "dsdkodsds---==-32=-3=2-32==32-32t32t23.0": False,
    "asdfokiiaweKOFEOWEFEFW:00.21": False,
    "12:32:12.00": False,
    "32:12.00.00": False,
    "2.00.00": False,
    "22:00.00": True,
}

test_counter = 0
for k, v in test_cases.items():
    correct_cases = len(test_cases)
    result, _ = is_valid_time_format(k)
    if result == v:
        test_counter += 1
    else:
        print("[Time Service] Test case failed", k, "Expected:", v)

print(f"[Time Service] {test_counter}/{correct_cases} test cases passed.")
