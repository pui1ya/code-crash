"""
====================================================
CrashReduce Inverted Index Benchmark
====================================================

Measures:

1. Index Creation Time
2. Documents Processed
3. Unique Terms Indexed
4. Memory Usage
5. Worker Utilization
6. Index Throughput

Outputs:

benchmark/reports/inverted_index_report.json

====================================================
"""

from pathlib import Path

import json
import time
import requests
import psutil


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
# Submit Job
# ====================================================

def submit_inverted_index_job():

    payload = {

        "job_type":
        "INVERTED_INDEX",

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
# Memory Usage
# ====================================================

def get_memory_usage_mb():

    process = psutil.Process()

    memory_bytes = (
        process.memory_info().rss
    )

    return round(

        memory_bytes
        /
        (1024 * 1024),

        2
    )


# ====================================================
# Build Report
# ====================================================

def generate_report(

    job,

    execution_time,

    utilization,

    memory_usage
):

    documents_processed = job.get(

        "documents_processed",

        0
    )

    unique_terms = job.get(

        "unique_terms",

        0
    )

    index_size_mb = job.get(

        "index_size_mb",

        0
    )

    throughput = 0

    if execution_time > 0:

        throughput = round(

            unique_terms
            /
            execution_time,

            2
        )

    report = {

        "job_id":
            job["job_id"],

        "job_type":
            "INVERTED_INDEX",

        "status":
            job["status"],

        "execution_time_seconds":
            round(
                execution_time,
                2
            ),

        "documents_processed":
            documents_processed,

        "unique_terms":
            unique_terms,

        "memory_usage_mb":
            memory_usage,

        "index_size_mb":
            index_size_mb,

        "terms_per_second":
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
        "inverted_index_report.json"
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
        "\n=== CrashReduce Inverted Index Benchmark ===\n"
    )

    start_time = time.time()

    job_response = (
        submit_inverted_index_job()
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

    memory_usage = (
        get_memory_usage_mb()
    )

    report = generate_report(

        job,

        execution_time,

        utilization,

        memory_usage
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
        "inverted_index_report.json"
    )


if __name__ == "__main__":

    main()