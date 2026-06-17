"""
====================================================
CrashReduce WordCount Benchmark
====================================================

Measures:

1. Execution Time
2. Throughput
3. Worker Utilization
4. Task Completion Metrics

Outputs:

benchmark/reports/wordcount_report.json

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
# Submit WordCount Job
# ====================================================

def submit_wordcount_job():

    payload = {

        "job_type": "WORDCOUNT",

        "input_path":
        "benchmark/wikipedia"
    }

    response = requests.post(

        f"{COORDINATOR_URL}/jobs",

        json=payload
    )

    response.raise_for_status()

    return response.json()


# ====================================================
# Poll Until Job Completes
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

        status = job["status"]

        print(
            f"[BENCHMARK] "
            f"Job={job_id} "
            f"Status={status}"
        )

        if status in (
            "COMPLETED",
            "FAILED"
        ):
            return job

        time.sleep(
            POLL_INTERVAL
        )


# ====================================================
# Fetch Cluster Metrics
# ====================================================

def get_cluster_metrics():

    response = requests.get(

        f"{COORDINATOR_URL}/metrics"
    )

    response.raise_for_status()

    return response.json()


# ====================================================
# Fetch Workers
# ====================================================

def get_workers():

    response = requests.get(

        f"{COORDINATOR_URL}/workers"
    )

    response.raise_for_status()

    return response.json()


# ====================================================
# Calculate Worker Utilization
# ====================================================

def calculate_worker_utilization(
    workers
):

    if not workers:
        return 0

    busy_workers = sum(

        1

        for worker in workers

        if worker["status"]
        == "BUSY"
    )

    return round(

        (
            busy_workers
            /
            len(workers)
        ) * 100,

        2
    )


# ====================================================
# Generate Benchmark Report
# ====================================================

def generate_report(

    job,

    execution_time,

    metrics,

    utilization
):

    completed_tasks = metrics.get(

        "completed_tasks",

        0
    )

    throughput = 0

    if execution_time > 0:

        throughput = round(

            completed_tasks
            /
            execution_time,

            2
        )

    report = {

        "job_id":
            job["job_id"],

        "job_type":
            "WORDCOUNT",

        "status":
            job["status"],

        "execution_time_seconds":
            round(
                execution_time,
                2
            ),

        "completed_tasks":
            completed_tasks,

        "throughput_tasks_per_second":
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
        "wordcount_report.json"
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
        "\n=== CrashReduce WordCount Benchmark ===\n"
    )

    start_time = time.time()

    job_response = (
        submit_wordcount_job()
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

    metrics = (
        get_cluster_metrics()
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

        metrics,

        utilization
    )

    print("\nBenchmark Results\n")

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
        "wordcount_report.json"
    )


if __name__ == "__main__":

    main()