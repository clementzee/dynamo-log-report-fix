Read the access log at `/app/access.log` and write a JSON summary report to `/app/report.json`.

The report must be a JSON object with exactly these keys:

1. `total_requests`: the number of non-empty log entries in `/app/access.log`.
2. `unique_ips`: the number of distinct client IP addresses. The client IP address is the first whitespace-separated field on each non-empty log line.
3. `top_path`: the request path that appears most often. The request appears inside quotes in the form `METHOD PATH PROTOCOL`; use only the `PATH` value. If multiple paths tie, choose the tied path that appears earliest in the log.

Do not include extra keys in the JSON report.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.