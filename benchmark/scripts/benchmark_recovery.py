"""
====================================================
CrashReduce Recovery Benchmark
====================================================

Scenario:

1. Start Cluster
2. Submit Job
3. Kill Worker
4. Measure Recovery
5. Verify Job Completion

Outputs:

benchmark/reports/recovery_report.json

====================================================
"""

from pathlib import Path

import json
import subprocess
import time
import requests


# ====================================================
# Configuration
# ====================================================

COORDINATOR_URL = "http://localhost:8000"

POLL_INTERVAL = 2

WORKER_TO_KILL = "crashreduce-worker-2"

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

def submit_job():

    payload = {

        "job_type":
        "WORDCOUNT",

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
# Kill Worker
# ====================================================

def kill_worker():

    print(
        f"\n[RECOVERY] "
        f"Killing {WORKER_TO_KILL}\n"
    )

    subprocess.run(

        [
            "docker",
            "stop",
            WORKER_TO_KILL
        ],

        check=False
    )


# ====================================================
# Wait Until Worker Dead
# ====================================================

def wait_for_worker_death():

    start = time.time()

    while True:

        workers = requests.get(

            f"{COORDINATOR_URL}/workers"
        ).json()

        for worker in workers:

            if (
                worker["worker_id"]
                ==
                WORKER_TO_KILL
            ):

                if (
                    worker["status"]
                    ==
                    "DEAD"
                ):

                    return (
                        time.time()
                        -
                        start
                    )

        time.sleep(
            POLL_INTERVAL
        )


# ====================================================
# Wait Until Recovery Event
# ====================================================

def wait_for_recovery():

    start = time.time()

    while True:

        events = requests.get(

            f"{COORDINATOR_URL}/recovery"
        ).json()

        for event in events:

            if (
                event[
                    "event_type"
                ]
                ==
                "TASK_REASSIGNED"
            ):

                return (
                    time.time()
                    -
                    start
                )

        time.sleep(
            POLL_INTERVAL
        )


# ====================================================
# Wait For Job Completion
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

            f"[RECOVERY] "

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
# Generate Report
# ====================================================

def generate_report(

    job,

    detection_time,

    reassignment_time,

    total_recovery_time
):

    success = (

        job["status"]
        ==
        "COMPLETED"
    )

    report = {

        "job_id":
            job["job_id"],

        "job_completed":
            success,

        "worker_killed":
            WORKER_TO_KILL,

        "failure_detection_seconds":
            round(
                detection_time,
                2
            ),

        "task_reassignment_seconds":
            round(
                reassignment_time,
                2
            ),

        "total_recovery_seconds":
            round(
                total_recovery_time,
                2
            ),

        "recovery_success":
            success,

        "timestamp":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }

    report_path = (

        REPORT_DIR
        /
        "recovery_report.json"
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
        "\n=== CrashReduce Recovery Benchmark ===\n"
    )

    job_response = (
        submit_job()
    )

    job_id = (
        job_response["job_id"]
    )

    print(
        f"Submitted Job: {job_id}"
    )

    # Give workers time
    # to start processing

    time.sleep(10)

    recovery_start = (
        time.time()
    )

    kill_worker()

    detection_time = (
        wait_for_worker_death()
    )

    reassignment_time = (
        wait_for_recovery()
    )

    job = wait_for_completion(
        job_id
    )

    total_recovery_time = (

        time.time()
        -
        recovery_start
    )

    report = generate_report(

        job,

        detection_time,

        reassignment_time,

        total_recovery_time
    )

    print(
        "\nRecovery Benchmark Results\n"
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
        "recovery_report.json"
    )


if __name__ == "__main__":

    main()