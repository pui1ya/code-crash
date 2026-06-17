"""
====================================================
CrashReduce Benchmark Report Generator
====================================================

Reads:

- wordcount_report.json
- grep_report.json
- inverted_index_report.json
- recovery_report.json

Generates:

- benchmark_summary.json
- benchmark_summary.csv
- benchmark_summary.md

====================================================
"""

from pathlib import Path

import csv
import json


# ====================================================
# Paths
# ====================================================

REPORTS_DIR = (
    Path(__file__)
    .parent
    .parent
    / "reports"
)

OUTPUT_JSON = (
    REPORTS_DIR
    / "benchmark_summary.json"
)

OUTPUT_CSV = (
    REPORTS_DIR
    / "benchmark_summary.csv"
)

OUTPUT_MD = (
    REPORTS_DIR
    / "benchmark_summary.md"
)


# ====================================================
# Load Report
# ====================================================

def load_report(filename):

    path = (
        REPORTS_DIR
        / filename
    )

    if not path.exists():

        print(
            f"[WARNING] "
            f"Missing {filename}"
        )

        return None

    with open(
        path,
        "r"
    ) as file:

        return json.load(
            file
        )


# ====================================================
# Collect Reports
# ====================================================

def collect_reports():

    reports = []

    files = [

        "wordcount_report.json",

        "grep_report.json",

        "inverted_index_report.json",

        "recovery_report.json"
    ]

    for filename in files:

        report = load_report(
            filename
        )

        if report:

            reports.append(
                report
            )

    return reports


# ====================================================
# Save JSON
# ====================================================

def save_json(
    reports
):

    with open(
        OUTPUT_JSON,
        "w"
    ) as file:

        json.dump(

            reports,

            file,

            indent=4
        )

    print(
        f"[OK] JSON -> "
        f"{OUTPUT_JSON}"
    )


# ====================================================
# Save CSV
# ====================================================

def save_csv(
    reports
):

    if not reports:
        return

    all_keys = set()

    for report in reports:

        all_keys.update(
            report.keys()
        )

    fieldnames = sorted(
        list(all_keys)
    )

    with open(
        OUTPUT_CSV,

        "w",

        newline=""
    ) as csv_file:

        writer = csv.DictWriter(

            csv_file,

            fieldnames=fieldnames
        )

        writer.writeheader()

        for report in reports:

            writer.writerow(
                report
            )

    print(
        f"[OK] CSV -> "
        f"{OUTPUT_CSV}"
    )


# ====================================================
# Save Markdown
# ====================================================

def save_markdown(
    reports
):

    lines = []

    lines.append(
        "# CrashReduce Benchmark Results\n"
    )

    lines.append(
        "Generated automatically from benchmark runs.\n"
    )

    for report in reports:

        lines.append(
            f"## {report.get('job_type', 'UNKNOWN')}\n"
        )

        for key, value in report.items():

            lines.append(
                f"- **{key}**: {value}"
            )

        lines.append("\n")

    with open(
        OUTPUT_MD,
        "w"
    ) as file:

        file.write(
            "\n".join(
                lines
            )
        )

    print(
        f"[OK] Markdown -> "
        f"{OUTPUT_MD}"
    )


# ====================================================
# Summary Statistics
# ====================================================

def print_summary(
    reports
):

    print(
        "\n=== BENCHMARK SUMMARY ===\n"
    )

    for report in reports:

        print(

            f"{report.get('job_type', 'UNKNOWN')} "

            f"-> "

            f"{report.get('status', 'N/A')}"
        )

    print()


# ====================================================
# Main
# ====================================================

def main():

    print(
        "\nGenerating Benchmark Reports...\n"
    )

    reports = (
        collect_reports()
    )

    if not reports:

        print(
            "No reports found."
        )

        return

    save_json(
        reports
    )

    save_csv(
        reports
    )

    save_markdown(
        reports
    )

    print_summary(
        reports
    )

    print(
        "Done."
    )


if __name__ == "__main__":

    main()