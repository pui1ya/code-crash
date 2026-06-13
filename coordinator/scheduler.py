
"""
CrashReduce Scheduler

Purpose
--------------------------------------------------

Responsible for deciding which worker gets which task.

The scheduler:

1. Looks for pending tasks
2. Finds available workers
3. Assigns tasks
4. Marks workers busy
5. Marks tasks running
6. Reassigns failed tasks

This module NEVER executes tasks.

Execution happens on worker nodes.

--------------------------------------------------
Scheduling Algorithm (V1)

FIFO Scheduling

Pending Tasks Queue
        ↓
First Available Worker
        ↓
Assign Task

Later versions can support:

- Round Robin
- Least Loaded Worker
- Data Locality Aware Scheduling
- Priority Scheduling
"""

from datetime import datetime
from typing import Dict, List, Optional


class Scheduler:
    """
    Main scheduler class.

    Receives references to:

    workers dictionary
    tasks dictionary

    and performs scheduling decisions.
    """

    def __init__(
        self,
        workers: Dict,
        tasks: Dict
    ):
        """
        Example:

        workers = {
            worker_id: worker_data
        }

        tasks = {
            task_id: task_data
        }
        """

        self.workers = workers
        self.tasks = tasks

    # ==================================================
    # WORKER SELECTION
    # ==================================================

    def find_available_worker(self) -> Optional[str]:
        """
        Finds the first idle worker.

        Returns:
            worker_id

        Returns None if no worker is available.
        """

        for worker_id, worker in self.workers.items():

            if worker["status"] == "IDLE":
                return worker_id

        return None

    # ==================================================
    # TASK SELECTION
    # ==================================================

    def get_pending_tasks(self) -> List[dict]:
        """
        Returns all pending tasks.

        Example:

        [
            task1,
            task2,
            task3
        ]
        """

        pending_tasks = []

        for task in self.tasks.values():

            if task["status"] == "PENDING":
                pending_tasks.append(task)

        return pending_tasks

    # ==================================================
    # ASSIGN SINGLE TASK
    # ==================================================

    def assign_task(
        self,
        task_id: str,
        worker_id: str
    ) -> bool:
        """
        Assign a task to a worker.

        Updates:

        task status
        worker status

        Returns:
            True if successful
        """

        if task_id not in self.tasks:
            return False

        if worker_id not in self.workers:
            return False

        task = self.tasks[task_id]
        worker = self.workers[worker_id]

        # Mark task running
        task["status"] = "RUNNING"

        task["assigned_worker"] = worker_id

        task["started_at"] = datetime.utcnow()

        # Mark worker busy
        worker["status"] = "BUSY"

        worker["current_task"] = task_id

        return True

    # ==================================================
    # MAIN SCHEDULER LOOP
    # ==================================================

    def schedule(self):
        """
        Core scheduling function.

        Called periodically.

        Flow:

        Find pending task
              ↓
        Find idle worker
              ↓
        Assign task
        """

        pending_tasks = self.get_pending_tasks()

        if not pending_tasks:
            return

        for task in pending_tasks:

            worker_id = self.find_available_worker()

            if worker_id is None:
                break

            self.assign_task(
                task_id=task["task_id"],
                worker_id=worker_id
            )

    # ==================================================
    # TASK COMPLETION
    # ==================================================

    def complete_task(
        self,
        task_id: str
    ):
        """
        Called when worker finishes task.

        Marks:

        task -> COMPLETED
        worker -> IDLE
        """

        if task_id not in self.tasks:
            return

        task = self.tasks[task_id]

        worker_id = task.get("assigned_worker")

        task["status"] = "COMPLETED"

        task["completed_at"] = datetime.utcnow()

        if worker_id:

            self.workers[worker_id]["status"] = "IDLE"

            self.workers[worker_id]["current_task"] = None

    # ==================================================
    # TASK FAILURE
    # ==================================================

    def fail_task(
        self,
        task_id: str
    ):
        """
        Called when:

        Worker crashes
        Worker timeout occurs

        Task becomes pending again
        so it can be reassigned.
        """

        if task_id not in self.tasks:
            return

        task = self.tasks[task_id]

        worker_id = task.get("assigned_worker")

        task["status"] = "PENDING"

        task["assigned_worker"] = None

        retries = task.get("retries", 0)

        task["retries"] = retries + 1

        if worker_id and worker_id in self.workers:

            self.workers[worker_id]["status"] = "DEAD"

            self.workers[worker_id]["current_task"] = None

    # ==================================================
    # REASSIGN FAILED TASKS
    # ==================================================

    def recover_failed_tasks(self):
        """
        Finds tasks that became pending again.

        Attempts reassignment.
        """

        self.schedule()

    # ==================================================
    # CLUSTER SUMMARY
    # ==================================================

    def cluster_status(self):
        """
        Useful for monitoring.

        Returns statistics.
        """

        total_workers = len(self.workers)

        idle_workers = len(
            [
                w
                for w in self.workers.values()
                if w["status"] == "IDLE"
            ]
        )

        busy_workers = len(
            [
                w
                for w in self.workers.values()
                if w["status"] == "BUSY"
            ]
        )

        pending_tasks = len(
            [
                t
                for t in self.tasks.values()
                if t["status"] == "PENDING"
            ]
        )

        running_tasks = len(
            [
                t
                for t in self.tasks.values()
                if t["status"] == "RUNNING"
            ]
        )

        completed_tasks = len(
            [
                t
                for t in self.tasks.values()
                if t["status"] == "COMPLETED"
            ]
        )

        return {
            "total_workers": total_workers,
            "idle_workers": idle_workers,
            "busy_workers": busy_workers,
            "pending_tasks": pending_tasks,
            "running_tasks": running_tasks,
            "completed_tasks": completed_tasks
        }