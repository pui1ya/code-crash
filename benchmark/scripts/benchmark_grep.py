"""
====================================================
CrashReduce Distributed Grep Benchmark
====================================================

Measures:

1. Search Time
2. Matches Found
3. Throughput
4. Worker Utilization
5. Files Scanned

Outputs:

benchmark/reports/grep_report.json

====================================================
"""

from pathlib import Path

import json
import time
import requests


# ====================================================
# Configuration
# ====================================================

COORDINATOR_URL = "http://localhost:8000"

SEARCH_TERM = "machine learning"

POLL_INTERVAL = 2

REPORT_DIR = (
    Path(__file__)
    .parent
    .parent
    / "reports"
)

REPORT_DIR.mkdir(
    exist_ok=True
)


# ====================================================
# Submit Grep Job
# ====================================================

def submit_grep_job():

    payload = {

        "job_type": "GREP",

        "input_path":
        "benchmark/wikipedia",

        "search_term":
        SEARCH_TERM
    }

    response = requests.post(

        f"{COORDINATOR_URL}/jobs",

        json=payload
    )

    response.raise_for_status()

    return response.json()


# ====================================================
# Wait For Completion
# ====================================================

def wait_for_completion(
    job_id
):

    while True:

        response = requests.get(

            f"{COORDINATOR_URL}/jobs/{job_id}"
        )

        response.raise_for_status()

        job = response.json()

        print(

            f"[BENCHMARK] "

            f"Job={job_id} "

            f"Status={job['status']}"
        )

        if job["status"] in (

            "COMPLETED",

            "FAILED"
        ):
            return job

        time.sleep(
            POLL_INTERVAL
        )


# ====================================================
# Cluster Metrics
# ====================================================

def get_cluster_metrics():

    response = requests.get(

        f"{COORDINATOR_URL}/metrics"
    )

    response.raise_for_status()

    return response.json()


# ====================================================
# Worker Metrics
# ====================================================

def get_workers():

    response = requests.get(

        f"{COORDINATOR_URL}/workers"
    )

    response.raise_for_status()

    return response.json()


# ====================================================
# Worker Utilization
# ====================================================

def calculate_worker_utilization(
    workers
):

    if not workers:
        return 0

    busy = sum(

        1

        for worker in workers

        if worker["status"]
        == "BUSY"
    )

    return round(

        (
            busy
            /
            len(workers)
        ) * 100,

        2
    )


# ====================================================
# Build Report
# ====================================================

def generate_report(

    job,

    execution_time,

    utilization
):

    matches_found = job.get(

        "matches_found",

        0
    )

    files_scanned = job.get(

        "files_scanned",

        0
    )

    throughput = 0

    if execution_time > 0:

        throughput = round(

            files_scanned
            /
            execution_time,

            2
        )

    report = {

        "job_id":
            job["job_id"],

        "job_type":
            "GREP",

        "search_term":
            SEARCH_TERM,

        "status":
            job["status"],

        "execution_time_seconds":
            round(
                execution_time,
                2
            ),

        "matches_found":
            matches_found,

        "files_scanned":
            files_scanned,

        "throughput_files_per_second":
            throughput,

        "worker_utilization_percent":
            utilization,

        "timestamp":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }

    report_path = (

        REPORT_DIR
        /
        "grep_report.json"
    )

    with open(
        report_path,
        "w"
    ) as file:

        json.dump(

            report,

            file,

            indent=4
        )

    return report


# ====================================================
# Main
# ====================================================

def main():

    print(
        "\n=== CrashReduce Grep Benchmark ===\n"
    )

    start_time = time.time()

    job_response = (
        submit_grep_job()
    )

    job_id = (
        job_response["job_id"]
    )

    print(
        f"Submitted Job: {job_id}"
    )

    job = wait_for_completion(
        job_id
    )

    end_time = time.time()

    execution_time = (
        end_time -
        start_time
    )

    workers = (
        get_workers()
    )

    utilization = (
        calculate_worker_utilization(
            workers
        )
    )

    report = generate_report(

        job,

        execution_time,

        utilization
    )

    print(
        "\nBenchmark Results\n"
    )

    print(
        json.dumps(
            report,
            indent=4
        )
    )

    print(
        "\nReport saved to:"
    )

    print(
        REPORT_DIR
        /
        "grep_report.json"
    )


if __name__ == "__main__":

    main()