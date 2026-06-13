
"""
CrashReduce Global Constants

Purpose
--------------------------------------------------

Single source of truth for:

- Heartbeat settings
- Scheduler settings
- Retry settings
- Storage paths
- API configuration
- Cluster defaults

Used by:

- Coordinator
- Workers
- Dashboard
"""

from pathlib import Path


# ==================================================
# PROJECT ROOT
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ==================================================
# STORAGE PATHS
# ==================================================

STORAGE_DIR = PROJECT_ROOT / "storage"

INPUT_DIR = STORAGE_DIR / "input"

INTERMEDIATE_DIR = STORAGE_DIR / "intermediate"

OUTPUT_DIR = STORAGE_DIR / "output"


# ==================================================
# COORDINATOR CONFIG
# ==================================================

COORDINATOR_HOST = "0.0.0.0"

COORDINATOR_PORT = 8000

COORDINATOR_URL = (
    f"http://localhost:{COORDINATOR_PORT}"
)


# ==================================================
# WORKER CONFIG
# ==================================================

DEFAULT_WORKER_PORT = 9001

WORKER_NAME_PREFIX = "worker"

MAX_WORKERS = 100


# ==================================================
# HEARTBEAT SETTINGS
# ==================================================

# Worker sends heartbeat every N seconds
HEARTBEAT_INTERVAL = 5

# Worker considered dead after N seconds
WORKER_TIMEOUT = 15

# Coordinator checks workers every N seconds
HEARTBEAT_CHECK_INTERVAL = 5


# ==================================================
# TASK SETTINGS
# ==================================================

MAX_TASK_RETRIES = 3

TASK_POLL_INTERVAL = 3

TASK_ASSIGNMENT_BATCH_SIZE = 1

TASK_TIMEOUT = 300
# 5 minutes


# ==================================================
# JOB SETTINGS
# ==================================================

DEFAULT_MAP_PARTITIONS = 4

DEFAULT_REDUCE_PARTITIONS = 2

MAX_MAP_PARTITIONS = 1000

MAX_REDUCE_PARTITIONS = 100


# ==================================================
# SCHEDULER SETTINGS
# ==================================================

SCHEDULER_INTERVAL = 2

SCHEDULER_STRATEGY_FIFO = "FIFO"

SCHEDULER_STRATEGY_ROUND_ROBIN = (
    "ROUND_ROBIN"
)

DEFAULT_SCHEDULER_STRATEGY = (
    SCHEDULER_STRATEGY_FIFO
)


# ==================================================
# FILE PARTITIONING
# ==================================================

DEFAULT_CHUNK_SIZE_MB = 64

MAX_CHUNK_SIZE_MB = 256


# ==================================================
# MAPPER SETTINGS
# ==================================================

DEFAULT_NUM_REDUCERS = 2

HASH_ALGORITHM = "md5"


# ==================================================
# REDUCER SETTINGS
# ==================================================

MERGE_OUTPUTS = True


# ==================================================
# API ROUTES
# ==================================================

REGISTER_WORKER_ROUTE = (
    "/workers/register"
)

WORKER_HEARTBEAT_ROUTE = (
    "/workers/heartbeat"
)

SUBMIT_JOB_ROUTE = (
    "/jobs/submit"
)

GET_JOBS_ROUTE = (
    "/jobs"
)

GET_WORKERS_ROUTE = (
    "/workers"
)

HEALTH_ROUTE = (
    "/health"
)


# ==================================================
# JOB TYPES
# ==================================================

WORDCOUNT_JOB = "WORDCOUNT"

INVERTED_INDEX_JOB = (
    "INVERTED_INDEX"
)

GREP_JOB = "GREP"


# ==================================================
# TASK TYPES
# ==================================================

MAP_TASK = "MAP"

REDUCE_TASK = "REDUCE"


# ==================================================
# TASK STATES
# ==================================================

TASK_PENDING = "PENDING"

TASK_RUNNING = "RUNNING"

TASK_COMPLETED = "COMPLETED"

TASK_FAILED = "FAILED"


# ==================================================
# WORKER STATES
# ==================================================

WORKER_IDLE = "IDLE"

WORKER_BUSY = "BUSY"

WORKER_DEAD = "DEAD"


# ==================================================
# JOB STATES
# ==================================================

JOB_SUBMITTED = "SUBMITTED"

JOB_MAP_PHASE = "MAP_PHASE"

JOB_MAP_COMPLETE = "MAP_COMPLETE"

JOB_REDUCE_PHASE = "REDUCE_PHASE"

JOB_REDUCE_COMPLETE = "REDUCE_COMPLETE"

JOB_COMPLETED = "COMPLETED"

JOB_FAILED = "FAILED"


# ==================================================
# MONITORING SETTINGS
# ==================================================

METRICS_COLLECTION_INTERVAL = 10

ENABLE_PROMETHEUS = True

ENABLE_GRAFANA = True


# ==================================================
# LOGGING
# ==================================================

LOG_LEVEL = "INFO"

LOG_FORMAT = (
    "%(asctime)s - "
    "%(name)s - "
    "%(levelname)s - "
    "%(message)s"
)

LOG_FILE = "crashreduce.log"


# ==================================================
# DOCKER SETTINGS
# ==================================================

DOCKER_NETWORK_NAME = (
    "crashreduce-network"
)

COORDINATOR_CONTAINER_NAME = (
    "coordinator"
)

WORKER_CONTAINER_PREFIX = (
    "worker"
)


# ==================================================
# BENCHMARK SETTINGS
# ==================================================

BENCHMARK_RESULTS_DIR = (
    PROJECT_ROOT
    / "benchmark"
    / "reports"
)

WIKIPEDIA_DATASET_DIR = (
    PROJECT_ROOT
    / "benchmark"
    / "wikipedia"
)


# ==================================================
# DEVELOPMENT SETTINGS
# ==================================================

DEBUG = True

AUTO_RELOAD = True

MOCK_WORKERS = False


# ==================================================
# VERSION INFO
# ==================================================

PROJECT_NAME = "CrashReduce"

VERSION = "1.0.0"

AUTHOR = "Punya"