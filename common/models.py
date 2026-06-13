
"""
CrashReduce Shared Data Models

Purpose
--------------------------------------------------

Defines the core entities used by the entire system.

These models are shared by:

- Coordinator
- Workers
- Dashboard
- API Endpoints

--------------------------------------------------

Core Models

1. Worker
2. Task
3. Job
4. Heartbeat
"""

from datetime import datetime
from typing import Optional
from typing import List
from typing import Dict
from enum import Enum

from pydantic import BaseModel
from pydantic import Field


# ==================================================
# ENUMS
# ==================================================

class WorkerStatus(str, Enum):
    """
    Valid worker states.
    """

    IDLE = "IDLE"

    BUSY = "BUSY"

    DEAD = "DEAD"


class TaskStatus(str, Enum):
    """
    Valid task states.
    """

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


class TaskType(str, Enum):
    """
    MapReduce task type.
    """

    MAP = "MAP"

    REDUCE = "REDUCE"


class JobStatus(str, Enum):
    """
    Job lifecycle.
    """

    SUBMITTED = "SUBMITTED"

    MAP_PHASE = "MAP_PHASE"

    MAP_COMPLETE = "MAP_COMPLETE"

    REDUCE_PHASE = "REDUCE_PHASE"

    REDUCE_COMPLETE = "REDUCE_COMPLETE"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


class JobType(str, Enum):
    """
    Supported jobs.
    """

    WORDCOUNT = "WORDCOUNT"

    INVERTED_INDEX = "INVERTED_INDEX"

    GREP = "GREP"


# ==================================================
# WORKER MODEL
# ==================================================

class Worker(BaseModel):
    """
    Worker node metadata.
    """

    worker_id: str

    worker_name: str

    host: str

    port: int

    status: WorkerStatus = WorkerStatus.IDLE

    current_task: Optional[str] = None

    tasks_completed: int = 0

    tasks_failed: int = 0

    registered_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    last_heartbeat: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==================================================
# TASK MODEL
# ==================================================

class Task(BaseModel):
    """
    Map or Reduce task.
    """

    task_id: str

    job_id: str

    task_type: TaskType

    job_type: JobType

    partition_id: int

    input_file: str

    status: TaskStatus = TaskStatus.PENDING

    assigned_worker: Optional[str] = None

    retries: int = 0

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None


# ==================================================
# JOB MODEL
# ==================================================

class Job(BaseModel):
    """
    Job submitted to coordinator.
    """

    job_id: str

    job_type: JobType

    input_file: str

    status: JobStatus = JobStatus.SUBMITTED

    map_partitions: int

    reduce_partitions: int

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    completed_at: Optional[datetime] = None


# ==================================================
# HEARTBEAT MODEL
# ==================================================

class Heartbeat(BaseModel):
    """
    Worker heartbeat payload.
    """

    worker_id: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )

    status: str = "ALIVE"


# ==================================================
# TASK RESULT MODEL
# ==================================================

class TaskResult(BaseModel):
    """
    Returned when worker
    completes a task.
    """

    task_id: str

    worker_id: str

    output_path: str

    completed_at: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==================================================
# TASK FAILURE MODEL
# ==================================================

class TaskFailure(BaseModel):
    """
    Sent when task execution fails.
    """

    task_id: str

    worker_id: str

    error_message: str

    failed_at: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==================================================
# JOB PROGRESS MODEL
# ==================================================

class JobProgress(BaseModel):
    """
    Dashboard progress model.
    """

    job_id: str

    total_tasks: int

    completed_tasks: int

    progress_percentage: float


# ==================================================
# CLUSTER SUMMARY MODEL
# ==================================================

class ClusterSummary(BaseModel):
    """
    Dashboard cluster metrics.
    """

    total_workers: int

    idle_workers: int

    busy_workers: int

    dead_workers: int

    total_jobs: int

    running_jobs: int

    completed_jobs: int


# ==================================================
# REDUCE OUTPUT MODEL
# ==================================================

class ReduceOutput(BaseModel):
    """
    Generic reducer output.
    """

    reducer_id: int

    output_file: str

    total_keys: int


# ==================================================
# SHUFFLE STATS MODEL
# ==================================================

class ShuffleStatistics(BaseModel):
    """
    Shuffle phase metrics.
    """

    reducer_partition: int

    total_keys: int

    total_values: int
