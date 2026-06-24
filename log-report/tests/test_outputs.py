import json
import re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")
REQUEST_RE = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH)\s+(\S+)\s+HTTP/[0-9.]+"')


def expected_summary():
    ips = set()
    path_counts = Counter()
    first_seen_order = {}
    total = 0

    for line in LOG_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue

        total += 1
        ips.add(line.split()[0])

        match = REQUEST_RE.search(line)
        assert match is not None, f"Could not parse request path from log line: {line!r}"

        path = match.group(1)
        if path not in first_seen_order:
            first_seen_order[path] = len(first_seen_order)
        path_counts[path] += 1

    top_path = sorted(
        path_counts,
        key=lambda path: (-path_counts[path], first_seen_order[path]),
    )[0]

    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": top_path,
    }


def load_report():
    assert REPORT_PATH.exists(), "Success criterion 1: /app/report.json must exist."
    return json.loads(REPORT_PATH.read_text())


def test_report_has_exact_schema():
    """Success criterion 1: /app/report.json is a JSON object with exactly total_requests, unique_ips, and top_path."""
    report = load_report()
    assert isinstance(report, dict)
    assert set(report.keys()) == {"total_requests", "unique_ips", "top_path"}


def test_report_value_types_are_correct():
    """Success criterion 2: total_requests and unique_ips are integers, and top_path is a string."""
    report = load_report()
    assert isinstance(report["total_requests"], int)
    assert isinstance(report["unique_ips"], int)
    assert isinstance(report["top_path"], str)


def test_report_values_match_access_log():
    """Success criterion 3: the report values match the summary recomputed from /app/access.log."""
    report = load_report()
    assert report == expected_summary()