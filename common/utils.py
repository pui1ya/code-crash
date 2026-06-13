
"""
CrashReduce Utility Functions

Purpose
--------------------------------------------------

Reusable helper functions shared by:

- Coordinator
- Workers
- Dashboard

These utilities should remain stateless.

--------------------------------------------------

Utilities Included

1. ID generation
2. Stable hashing
3. Timestamp helpers
4. JSON helpers
5. File helpers
6. Retry helpers
7. Chunking helpers
"""

import json
import hashlib
import time

from uuid import uuid4
from pathlib import Path
from datetime import datetime
from functools import wraps


# ==================================================
# ID HELPERS
# ==================================================

def generate_id() -> str:
    """
    Generate unique identifier.

    Example:
    4c3a0f67-....
    """

    return str(uuid4())


def generate_task_id() -> str:
    """
    Generate task id.
    """

    return f"task_{uuid4()}"


def generate_job_id() -> str:
    """
    Generate job id.
    """

    return f"job_{uuid4()}"


def generate_worker_id() -> str:
    """
    Generate worker id.
    """

    return f"worker_{uuid4()}"


# ==================================================
# TIME HELPERS
# ==================================================

def utc_now():
    """
    Current UTC timestamp.
    """

    return datetime.utcnow()


def utc_now_iso():
    """
    ISO formatted UTC timestamp.
    """

    return datetime.utcnow().isoformat()


def seconds_since(timestamp):
    """
    Returns elapsed seconds.
    """

    return (
        datetime.utcnow() - timestamp
    ).total_seconds()


# ==================================================
# HASHING
# ==================================================

def stable_hash(key: str) -> int:
    """
    Distributed-safe hash.

    IMPORTANT:

    Do NOT use Python's hash()
    because results differ between
    processes.

    Used for reducer partitioning.
    """

    return int(
        hashlib.md5(
            key.encode("utf-8")
        ).hexdigest(),
        16
    )


def get_partition(
    key: str,
    num_reducers: int
) -> int:
    """
    Determine reducer partition.

    Example:

    hello -> reducer 0
    world -> reducer 1
    """

    return (
        stable_hash(key)
        % num_reducers
    )


# ==================================================
# DIRECTORY HELPERS
# ==================================================

def ensure_directory(path):
    """
    Create directory if missing.
    """

    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )


# ==================================================
# JSON HELPERS
# ==================================================

def write_json(
    file_path,
    data
):
    """
    Save JSON to disk.
    """

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


def read_json(
    file_path
):
    """
    Read JSON from disk.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==================================================
# FILE HELPERS
# ==================================================

def file_exists(
    file_path
):
    """
    Check if file exists.
    """

    return Path(
        file_path
    ).exists()


def get_file_size_mb(
    file_path
):
    """
    File size in MB.
    """

    size = Path(
        file_path
    ).stat().st_size

    return size / (1024 * 1024)


# ==================================================
# FILE CHUNKING
# ==================================================

def chunk_file(
    input_file,
    num_chunks
):
    """
    Splits file logically.

    Returns list of chunks.

    Version 1:
    Returns line partitions.

    Later:
    Physical file splitting.
    """

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    chunk_size = (
        len(lines)
        // num_chunks
    )

    chunks = []

    for i in range(num_chunks):

        start = i * chunk_size

        if i == num_chunks - 1:

            end = len(lines)

        else:

            end = (
                start
                + chunk_size
            )

        chunks.append(
            lines[start:end]
        )

    return chunks


# ==================================================
# RETRY DECORATOR
# ==================================================

def retry(
    attempts=3,
    delay=1
):
    """
    Retry operation automatically.

    Useful for:

    Network requests
    Coordinator calls
    File operations
    """

    def decorator(func):

        @wraps(func)
        def wrapper(
            *args,
            **kwargs
        ):

            last_exception = None

            for _ in range(
                attempts
            ):

                try:

                    return func(
                        *args,
                        **kwargs
                    )

                except Exception as e:

                    last_exception = e

                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator


# ==================================================
# TASK HELPERS
# ==================================================

def is_map_task(task):
    """
    Convenience helper.
    """

    return (
        task["task_type"]
        == "MAP"
    )


def is_reduce_task(task):
    """
    Convenience helper.
    """

    return (
        task["task_type"]
        == "REDUCE"
    )


# ==================================================
# METRICS
# ==================================================

def calculate_progress(
    completed,
    total
):
    """
    Returns progress percentage.
    """

    if total == 0:

        return 0.0

    return round(
        (
            completed / total
        ) * 100,
        2
    )


# ==================================================
# LOGGING HELPERS
# ==================================================

def log_banner(
    title
):
    """
    Pretty startup logs.
    """

    line = "=" * 60

    print(line)

    print(title)

    print(line)


# ==================================================
# HEARTBEAT HELPERS
# ==================================================

def worker_timed_out(
    last_heartbeat,
    timeout_seconds
):
    """
    Determines if worker died.
    """

    return (
        seconds_since(
            last_heartbeat
        )
        > timeout_seconds
    )
