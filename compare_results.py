#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def summarize_result(data, filename):
    if data is None:
        return {
            "file": filename,
            "model_name": "N/A",
            "provider_name": "N/A",
            "secret_phrase": "N/A",
            "tasks_total": 0,
            "tasks_success": 0,
            "tasks_failure": 0,
            "tasks_not_supported": 0,
        }

    tasks = data.get("tasks", []) or []

    success = sum(1 for t in tasks if t.get("outcome") == "success")
    failure = sum(1 for t in tasks if t.get("outcome") == "failure")
    not_supported = sum(1 for t in tasks if t.get("outcome") == "not_supported")

    return {
        "file": filename,
        "model_name": data.get("model_name", "unknown"),
        "provider_name": data.get("provider_name", "unknown"),
        "reported_datetime": data.get("reported_datetime", "unknown"),
        "secret_phrase": data.get("secret_phrase", "missing"),
        "tasks_total": len(tasks),
        "tasks_success": success,
        "tasks_failure": failure,
        "tasks_not_supported": not_supported,
        "can_access_http": data.get("reported_capabilities", {}).get("can_access_http", None),
        "can_execute_code": data.get("reported_capabilities", {}).get("can_execute_code", None),
        "can_use_external_tools": data.get("reported_capabilities", {}).get("can_use_external_tools", None),
        "has_persistent_memory": data.get("reported_capabilities", {}).get("has_persistent_memory", None),
    }

def print_table(rows):
    if not rows:
        print("No results.")
        return

    # Choose columns to show
    cols = [
        "file",
        "model_name",
        "provider_name",
        "reported_datetime",
        "secret_phrase",
        "tasks_total",
        "tasks_success",
        "tasks_failure",
        "tasks_not_supported",
        "can_access_http",
        "can_execute_code",
        "can_use_external_tools",
        "has_persistent_memory",
    ]

    # Compute column widths
    col_widths = {c: len(c) for c in cols}
    for row in rows:
        for c in cols:
            val = row.get(c, "")
            text = str(val)
            if len(text) > col_widths[c]:
                col_widths[c] = len(text)

    # Print header
    header = " | ".join(c.ljust(col_widths[c]) for c in cols)
    sep = "-+-".join("-" * col_widths[c] for c in cols)
    print(header)
    print(sep)

    # Print rows
    for row in rows:
        line = " | ".join(str(row.get(c, "")).ljust(col_widths[c]) for c in cols)
        print(line)

def main():
    if len(sys.argv) < 2:
        print("Usage: python compare_results.py result1.json result2.json ...")
        sys.exit(1)

    rows = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        data = load_json(path)
        summary = summarize_result(data, path.name)
        rows.append(summary)

    print_table(rows)

if __name__ == "__main__":
    main()
