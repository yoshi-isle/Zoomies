import re


def is_valid_time_format(metric: str) -> bool:
    pattern = r"^\d+:\d{2}(\.\d{2})?$"
    return bool(re.match(pattern, metric.strip()))


test_cases = [
    "0:06",
    "0:06.00",
    "35:21",
    "1:23.45",
    "123:45",
    "0:00",
    "10:59.99",
]

for t in test_cases:
    print(f"{t:>12} -> {is_valid_time_format(t)}")
