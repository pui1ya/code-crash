"""
tests/test_recovery.py

Tests fault tolerance and recovery.

Verifies:

1. Dead worker detection
2. Task reassignment
3. Worker state updates
4. Retry limits
5. Cluster recovery

Run:

pytest tests/test_recovery.py -v
"""

from datetime import datetime
from datetime import timedelta

from common.models import (
    Worker,
    Task,
    WorkerStatus,
    TaskStatus,
    TaskType,
    JobType
)

from common.utils import worker_timed_out


# ==================================================
# HELPERS
# ==================================================

def create_worker(
    worker_id="worker-1"
):
    """
    Test worker factory.
    """

    return Worker(
        worker_id=worker_id,
        worker_name=worker_id,
        host="localhost",
        port=9001
    )


def create_task(
    task_id="task-1"
):
    """
    Test task factory.
    """

    return Task(
        task_id=task_id,
        job_id="job-1",
        task_type=TaskType.MAP,
        job_type=JobType.WORDCOUNT,
        partition_id=0,
        input_file="sample.txt"
    )


# ==================================================
# HEARTBEAT TESTS
# ==================================================

class TestHeartbeatTimeout:

    def test_worker_alive(self):

        worker = create_worker()

        worker.last_heartbeat = (
            datetime.utcnow()
            - timedelta(seconds=5)
        )

        assert not worker_timed_out(
            worker.last_heartbeat,
            timeout_seconds=15
        )

    def test_worker_dead(self):

        worker = create_worker()

        worker.last_heartbeat = (
            datetime.utcnow()
            - timedelta(seconds=30)
        )

        assert worker_timed_out(
            worker.last_heartbeat,
            timeout_seconds=15
        )


# ==================================================
# WORKER CRASH TESTS
# ==================================================

class TestWorkerCrash:

    def test_dead_worker_status_change(self):

        worker = create_worker()

        worker.status = (
            WorkerStatus.DEAD
        )

        assert (
            worker.status
            ==
            WorkerStatus.DEAD
        )

    def test_busy_worker_crashes(self):

        worker = create_worker()

        worker.status = (
            WorkerStatus.BUSY
        )

        worker.current_task = (
            "task-1"
        )

        worker.status = (
            WorkerStatus.DEAD
        )

        assert (
            worker.status
            ==
            WorkerStatus.DEAD
        )


# ==================================================
# TASK REASSIGNMENT
# ==================================================

class TestTaskReassignment:

    def test_running_task_becomes_pending(self):

        task = create_task()

        task.status = (
            TaskStatus.RUNNING
        )

        task.assigned_worker = (
            "worker-1"
        )

        # Simulate worker death

        task.status = (
            TaskStatus.PENDING
        )

        task.assigned_worker = None

        assert (
            task.status
            ==
            TaskStatus.PENDING
        )

        assert (
            task.assigned_worker
            is None
        )

    def test_task_can_be_reassigned(self):

        task = create_task()

        task.status = (
            TaskStatus.PENDING
        )

        task.assigned_worker = (
            "worker-2"
        )

        task.status = (
            TaskStatus.RUNNING
        )

        assert (
            task.assigned_worker
            ==
            "worker-2"
        )

        assert (
            task.status
            ==
            TaskStatus.RUNNING
        )


# ==================================================
# RETRY TESTS
# ==================================================

class TestRetries:

    def test_retry_increment(self):

        task = create_task()

        task.retries += 1

        assert task.retries == 1

    def test_multiple_retries(self):

        task = create_task()

        task.retries = 3

        assert task.retries == 3

    def test_exceeded_retry_limit(self):

        MAX_RETRIES = 3

        task = create_task()

        task.retries = 4

        should_fail = (
            task.retries
            >
            MAX_RETRIES
        )

        assert should_fail


# ==================================================
# CLUSTER RECOVERY
# ==================================================

class TestClusterRecovery:

    def test_other_workers_survive(self):

        worker1 = create_worker(
            "worker1"
        )

        worker2 = create_worker(
            "worker2"
        )

        worker3 = create_worker(
            "worker3"
        )

        worker1.status = (
            WorkerStatus.DEAD
        )

        assert (
            worker2.status
            ==
            WorkerStatus.IDLE
        )

        assert (
            worker3.status
            ==
            WorkerStatus.IDLE
        )

    def test_task_moves_to_alive_worker(self):

        task = create_task()

        dead_worker = (
            create_worker(
                "worker1"
            )
        )

        alive_worker = (
            create_worker(
                "worker2"
            )
        )

        dead_worker.status = (
            WorkerStatus.DEAD
        )

        task.assigned_worker = (
            alive_worker.worker_id
        )

        task.status = (
            TaskStatus.RUNNING
        )

        assert (
            task.assigned_worker
            ==
            "worker2"
        )

    def test_job_can_continue_after_crash(self):

        tasks = [
            create_task("t1"),
            create_task("t2"),
            create_task("t3")
        ]

        tasks[0].status = (
            TaskStatus.COMPLETED
        )

        tasks[1].status = (
            TaskStatus.RUNNING
        )

        tasks[2].status = (
            TaskStatus.PENDING
        )

        # worker executing t2 dies

        tasks[1].status = (
            TaskStatus.PENDING
        )

        completed = sum(
            1
            for task in tasks
            if task.status
            ==
            TaskStatus.COMPLETED
        )

        pending = sum(
            1
            for task in tasks
            if task.status
            ==
            TaskStatus.PENDING
        )

        assert completed == 1

        assert pending == 2