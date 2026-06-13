
"""
CrashReduce Worker Registry

Single source of truth for all workers.

Responsibilities
--------------------------------------------------

1. Register workers
2. Track worker metadata
3. Track status changes
4. Track current task assignment
5. Track heartbeats
6. Provide worker statistics

Every coordinator component should
access worker information through
this registry.

Used by:

- main.py
- scheduler.py
- heartbeat_monitor.py
- job_manager.py
"""

from datetime import datetime
from uuid import uuid4
from typing import Dict, List, Optional


class WorkerRegistry:
    """
    Central worker storage.
    """

    def __init__(self):
        """
        Stores workers in memory.

        Key:
            worker_id

        Value:
            worker metadata dictionary
        """

        self.workers: Dict[str, dict] = {}

    # ==================================================
    # REGISTER WORKER
    # ==================================================

    def register_worker(
        self,
        worker_name: str,
        host: str,
        port: int
    ) -> str:
        """
        Called when a worker starts.

        Returns:
            worker_id
        """

        worker_id = str(uuid4())

        self.workers[worker_id] = {
            "worker_id": worker_id,

            "worker_name": worker_name,

            "host": host,

            "port": port,

            "status": "IDLE",

            "current_task": None,

            "tasks_completed": 0,

            "tasks_failed": 0,

            "registered_at": datetime.utcnow(),

            "last_heartbeat": datetime.utcnow()
        }

        return worker_id

    # ==================================================
    # GET WORKER
    # ==================================================

    def get_worker(
        self,
        worker_id: str
    ) -> Optional[dict]:
        """
        Returns worker details.

        Returns None if not found.
        """

        return self.workers.get(worker_id)

    # ==================================================
    # GET ALL WORKERS
    # ==================================================

    def get_all_workers(self) -> Dict[str, dict]:
        """
        Returns entire worker registry.
        """

        return self.workers

    # ==================================================
    # UPDATE HEARTBEAT
    # ==================================================

    def update_heartbeat(
        self,
        worker_id: str
    ) -> bool:
        """
        Updates heartbeat timestamp.

        Returns:
            True if worker exists
            False otherwise
        """

        worker = self.get_worker(worker_id)

        if not worker:
            return False

        worker["last_heartbeat"] = datetime.utcnow()

        return True

    # ==================================================
    # UPDATE STATUS
    # ==================================================

    def update_status(
        self,
        worker_id: str,
        status: str
    ) -> bool:
        """
        Example statuses:

        IDLE
        BUSY
        DEAD
        """

        worker = self.get_worker(worker_id)

        if not worker:
            return False

        worker["status"] = status

        return True

    # ==================================================
    # ASSIGN TASK
    # ==================================================

    def assign_task(
        self,
        worker_id: str,
        task_id: str
    ) -> bool:
        """
        Worker becomes busy.
        """

        worker = self.get_worker(worker_id)

        if not worker:
            return False

        worker["current_task"] = task_id

        worker["status"] = "BUSY"

        return True

    # ==================================================
    # COMPLETE TASK
    # ==================================================

    def complete_task(
        self,
        worker_id: str
    ) -> bool:
        """
        Called when task finishes.
        """

        worker = self.get_worker(worker_id)

        if not worker:
            return False

        worker["current_task"] = None

        worker["status"] = "IDLE"

        worker["tasks_completed"] += 1

        return True

    # ==================================================
    # FAIL TASK
    # ==================================================

    def fail_task(
        self,
        worker_id: str
    ) -> bool:
        """
        Called when task execution fails.
        """

        worker = self.get_worker(worker_id)

        if not worker:
            return False

        worker["tasks_failed"] += 1

        worker["current_task"] = None

        worker["status"] = "IDLE"

        return True

    # ==================================================
    # MARK DEAD
    # ==================================================

    def mark_dead(
        self,
        worker_id: str
    ) -> bool:
        """
        Called by heartbeat monitor.
        """

        worker = self.get_worker(worker_id)

        if not worker:
            return False

        worker["status"] = "DEAD"

        return True

    # ==================================================
    # GET AVAILABLE WORKERS
    # ==================================================

    def get_available_workers(
        self
    ) -> List[dict]:
        """
        Returns all idle workers.
        """

        return [
            worker
            for worker in self.workers.values()
            if worker["status"] == "IDLE"
        ]

    # ==================================================
    # GET BUSY WORKERS
    # ==================================================

    def get_busy_workers(
        self
    ) -> List[dict]:
        """
        Returns all busy workers.
        """

        return [
            worker
            for worker in self.workers.values()
            if worker["status"] == "BUSY"
        ]

    # ==================================================
    # GET DEAD WORKERS
    # ==================================================

    def get_dead_workers(
        self
    ) -> List[dict]:
        """
        Returns dead workers.
        """

        return [
            worker
            for worker in self.workers.values()
            if worker["status"] == "DEAD"
        ]

    # ==================================================
    # REMOVE WORKER
    # ==================================================

    def remove_worker(
        self,
        worker_id: str
    ) -> bool:
        """
        Permanently remove worker.

        Usually not recommended.

        Useful during testing.
        """

        if worker_id not in self.workers:
            return False

        del self.workers[worker_id]

        return True

    # ==================================================
    # CLUSTER SUMMARY
    # ==================================================

    def get_cluster_summary(
        self
    ) -> dict:
        """
        Dashboard statistics.
        """

        total_workers = len(self.workers)

        idle_workers = len(
            self.get_available_workers()
        )

        busy_workers = len(
            self.get_busy_workers()
        )

        dead_workers = len(
            self.get_dead_workers()
        )

        return {
            "total_workers": total_workers,
            "idle_workers": idle_workers,
            "busy_workers": busy_workers,
            "dead_workers": dead_workers
        }

    # ==================================================
    # WORKER PERFORMANCE
    # ==================================================

    def get_worker_statistics(
        self,
        worker_id: str
    ) -> Optional[dict]:
        """
        Returns performance metrics.
        """

        worker = self.get_worker(worker_id)

        if not worker:
            return None

        return {
            "worker_id": worker["worker_id"],

            "worker_name": worker["worker_name"],

            "tasks_completed":
                worker["tasks_completed"],

            "tasks_failed":
                worker["tasks_failed"],

            "status":
                worker["status"],

            "current_task":
                worker["current_task"]
        }