
"""
CrashReduce Communication Schemas

Purpose
--------------------------------------------------

Defines all messages exchanged between:

1. Coordinator
2. Workers
3. Dashboard

These schemas are used by:

- FastAPI endpoints
- Internal RPC calls
- Future gRPC migration

--------------------------------------------------

Messages

Worker Registration
Heartbeat
Task Assignment
Task Completion
Task Failure
Job Submission
Cluster Monitoring
"""

from datetime import datetime
from typing import Optional
from typing import List
from typing import Dict

from pydantic import BaseModel
from pydantic import Field

from common.models import JobType
from common.models import TaskType


# ==================================================
# WORKER REGISTRATION
# ==================================================

class RegisterWorkerRequest(BaseModel):
    """
    Worker → Coordinator

    Sent when worker starts.
    """

    worker_name: str

    host: str

    port: int


class RegisterWorkerResponse(BaseModel):
    """
    Coordinator → Worker

    Returns assigned worker id.
    """

    worker_id: str

    status: str = "REGISTERED"

    heartbeat_interval: int = 5


# ==================================================
# HEARTBEAT
# ==================================================

class HeartbeatRequest(BaseModel):
    """
    Worker → Coordinator

    Periodic health signal.
    """

    worker_id: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )

    status: str = "ALIVE"


class HeartbeatResponse(BaseModel):
    """
    Coordinator → Worker
    """

    accepted: bool

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==================================================
# JOB SUBMISSION
# ==================================================

class SubmitJobRequest(BaseModel):
    """
    Client → Coordinator
    """

    job_type: JobType

    input_file: str

    map_partitions: int = 4

    reduce_partitions: int = 2


class SubmitJobResponse(BaseModel):
    """
    Coordinator → Client
    """

    job_id: str

    status: str


# ==================================================
# TASK REQUEST
# ==================================================

class TaskRequest(BaseModel):
    """
    Worker → Coordinator

    Worker asks for work.
    """

    worker_id: str


# ==================================================
# TASK ASSIGNMENT
# ==================================================

class TaskAssignmentResponse(BaseModel):
    """
    Coordinator → Worker

    Assigns a task.
    """

    task_id: str

    job_id: str

    task_type: TaskType

    job_type: JobType

    partition_id: int

    input_file: str

    assigned_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    search_term: Optional[str] = None


# ==================================================
# NO TASK AVAILABLE
# ==================================================

class NoTaskResponse(BaseModel):
    """
    Coordinator → Worker

    Returned when queue is empty.
    """

    message: str = "NO_TASK_AVAILABLE"


# ==================================================
# TASK COMPLETE
# ==================================================

class TaskCompleteRequest(BaseModel):
    """
    Worker → Coordinator

    Sent when task finishes.
    """

    task_id: str

    worker_id: str

    output_path: str

    completed_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class TaskCompleteResponse(BaseModel):
    """
    Coordinator → Worker
    """

    acknowledged: bool

    message: str


# ==================================================
# TASK FAILURE
# ==================================================

class TaskFailureRequest(BaseModel):
    """
    Worker → Coordinator

    Sent when task fails.
    """

    task_id: str

    worker_id: str

    error_message: str

    failed_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class TaskFailureResponse(BaseModel):
    """
    Coordinator → Worker
    """

    acknowledged: bool

    retry_scheduled: bool


# ==================================================
# JOB STATUS
# ==================================================

class JobStatusResponse(BaseModel):
    """
    Dashboard → Coordinator
    """

    job_id: str

    status: str

    progress_percentage: float

    total_tasks: int

    completed_tasks: int


# ==================================================
# WORKER STATUS
# ==================================================

class WorkerStatusResponse(BaseModel):
    """
    Dashboard → Coordinator
    """

    worker_id: str

    worker_name: str

    status: str

    current_task: Optional[str]

    tasks_completed: int

    tasks_failed: int

    last_heartbeat: datetime


# ==================================================
# CLUSTER SUMMARY
# ==================================================

class ClusterSummaryResponse(BaseModel):
    """
    Dashboard Overview
    """

    total_workers: int

    idle_workers: int

    busy_workers: int

    dead_workers: int

    total_jobs: int

    running_jobs: int

    completed_jobs: int

    failed_jobs: int


# ==================================================
# HEALTH CHECK
# ==================================================

class HealthResponse(BaseModel):
    """
    Health endpoint response.
    """

    status: str

    service: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==================================================
# RECOVERY EVENT
# ==================================================

class RecoveryEvent(BaseModel):
    """
    Used for crash recovery logging.
    """

    worker_id: str

    task_id: str

    recovery_reason: str

    recovered_at: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==================================================
# SHUFFLE STATISTICS
# ==================================================

class ShuffleStatisticsResponse(BaseModel):
    """
    Debugging and monitoring.
    """

    reducer_partition: int

    total_keys: int

    total_values: int


# ==================================================
# EXECUTION METRICS
# ==================================================

class ExecutionMetricsResponse(BaseModel):
    """
    Performance metrics.
    """

    task_id: str

    execution_time_seconds: float

    cpu_usage_percent: Optional[float] = None

    memory_usage_mb: Optional[float] = None


# ==================================================
# ERROR RESPONSE
# ==================================================

class ErrorResponse(BaseModel):
    """
    Generic API error.
    """

    error_code: str

    message: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )