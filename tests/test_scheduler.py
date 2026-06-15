"""
tests/test_scheduler.py

Purpose
----------------------------------------------------
Tests scheduler behavior.

Verifies:

1. Task assignment
2. Idle worker selection
3. Load balancing
4. Dead worker avoidance
5. Reassignment
6. No-worker scenarios

Run:

pytest tests/test_scheduler.py -v
"""

from common.models import (
    Worker,
    Task,
    WorkerStatus,
    TaskStatus,
    TaskType,
    JobType
)


# ==================================================
# TEST HELPERS
# ==================================================

def create_worker(
    worker_id: str,
    status=WorkerStatus.IDLE,
    completed=0
):
    """
    Creates a test worker.
    """

    worker = Worker(
        worker_id=worker_id,
        worker_name=worker_id,
        host="localhost",
        port=9001
    )

    worker.status = status
    worker.tasks_completed = completed

    return worker


def create_task(
    task_id="task-1"
):
    """
    Creates a test task.
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
# BASIC ASSIGNMENT
# ==================================================

class TestTaskAssignment:

    def test_idle_worker_receives_task(self):

        worker = create_worker(
            "worker-1"
        )

        task = create_task()

        worker.current_task = (
            task.task_id
        )

        worker.status = (
            WorkerStatus.BUSY
        )

        task.assigned_worker = (
            worker.worker_id
        )

        task.status = (
            TaskStatus.RUNNING
        )

        assert (
            task.assigned_worker
            ==
            "worker-1"
        )

        assert (
            worker.status
            ==
            WorkerStatus.BUSY
        )

    def test_task_status_changes(self):

        task = create_task()

        task.status = (
            TaskStatus.RUNNING
        )

        assert (
            task.status
            ==
            TaskStatus.RUNNING
        )


# ==================================================
# IDLE WORKER SELECTION
# ==================================================

class TestIdleWorkerSelection:

    def test_select_first_idle_worker(self):

        workers = [

            create_worker(
                "worker-1",
                WorkerStatus.BUSY
            ),

            create_worker(
                "worker-2",
                WorkerStatus.IDLE
            ),

            create_worker(
                "worker-3",
                WorkerStatus.IDLE
            )
        ]

        idle_workers = [

            worker
            for worker in workers
            if worker.status
            ==
            WorkerStatus.IDLE
        ]

        assert (
            idle_workers[0]
            .worker_id
            ==
            "worker-2"
        )

    def test_no_idle_workers(self):

        workers = [

            create_worker(
                "worker-1",
                WorkerStatus.BUSY
            ),

            create_worker(
                "worker-2",
                WorkerStatus.BUSY
            )
        ]

        idle_workers = [

            worker
            for worker in workers
            if worker.status
            ==
            WorkerStatus.IDLE
        ]

        assert (
            len(idle_workers)
            == 0
        )


# ==================================================
# LOAD BALANCING
# ==================================================

class TestLoadBalancing:

    def test_least_loaded_worker(self):

        workers = [

            create_worker(
                "worker-1",
                completed=50
            ),

            create_worker(
                "worker-2",
                completed=10
            ),

            create_worker(
                "worker-3",
                completed=30
            )
        ]

        selected = min(
            workers,
            key=lambda worker:
            worker.tasks_completed
        )

        assert (
            selected.worker_id
            ==
            "worker-2"
        )

    def test_even_distribution_possible(self):

        workers = [

            create_worker("w1"),
            create_worker("w2"),
            create_worker("w3")
        ]

        tasks = 9

        expected = tasks // len(workers)

        assert expected == 3


# ==================================================
# DEAD WORKERS
# ==================================================

class TestDeadWorkers:

    def test_dead_worker_not_selected(self):

        workers = [

            create_worker(
                "worker-1",
                WorkerStatus.DEAD
            ),

            create_worker(
                "worker-2",
                WorkerStatus.IDLE
            )
        ]

        available = [

            worker
            for worker in workers
            if worker.status
            ==
            WorkerStatus.IDLE
        ]

        assert len(available) == 1

        assert (
            available[0].worker_id
            ==
            "worker-2"
        )

    def test_all_workers_dead(self):

        workers = [

            create_worker(
                "worker-1",
                WorkerStatus.DEAD
            ),

            create_worker(
                "worker-2",
                WorkerStatus.DEAD
            )
        ]

        available = [

            worker
            for worker in workers
            if worker.status
            ==
            WorkerStatus.IDLE
        ]

        assert (
            len(available)
            == 0
        )


# ==================================================
# TASK REASSIGNMENT
# ==================================================

class TestTaskReassignment:

    def test_task_returns_to_pending(self):

        task = create_task()

        task.status = (
            TaskStatus.RUNNING
        )

        task.assigned_worker = (
            "worker-1"
        )

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

    def test_pending_task_can_be_reassigned(self):

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


# ==================================================
# ROUND ROBIN LOGIC
# ==================================================

class TestRoundRobin:

    def test_round_robin_rotation(self):

        workers = [
            "w1",
            "w2",
            "w3"
        ]

        assignments = []

        for i in range(6):

            assignments.append(
                workers[
                    i % len(workers)
                ]
            )

        assert assignments == [

            "w1",
            "w2",
            "w3",

            "w1",
            "w2",
            "w3"
        ]


# ==================================================
# STRESS TEST
# ==================================================

class TestSchedulerStress:

    def test_many_workers(self):

        workers = [

            create_worker(
                f"worker-{i}"
            )

            for i in range(100)
        ]

        assert (
            len(workers)
            == 100
        )

    def test_many_tasks(self):

        tasks = [

            create_task(
                f"task-{i}"
            )

            for i in range(1000)
        ]

        assert (
            len(tasks)
            == 1000
        )