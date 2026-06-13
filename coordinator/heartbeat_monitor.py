
"""
CrashReduce Heartbeat Monitor

Purpose
----------------------------------------------------

Responsible for detecting dead workers.

Workers periodically send heartbeats.

If a worker stops sending heartbeats
for longer than WORKER_TIMEOUT,
the worker is declared DEAD.

Tasks that were running on the dead worker
are automatically marked for reassignment.

----------------------------------------------------

Example:

Worker-1 heartbeat received
Worker-2 heartbeat received
Worker-3 heartbeat received

Worker-2 crashes

After timeout:

Worker-2 => DEAD

Running task on Worker-2
becomes PENDING again

Scheduler can reassign it.
"""

from datetime import datetime
from typing import Dict, List, Optional


class HeartbeatMonitor:
    """
    Monitors worker health.

    Depends on:

    worker_registry
    task_manager
    """

    def __init__(
        self,
        worker_registry,
        task_manager,
        worker_timeout: int = 15
    ):
        """
        Parameters
        ----------

        worker_registry:
            Central worker registry

        task_manager:
            Used to recover tasks

        worker_timeout:
            Maximum allowed time
            without heartbeat.
        """

        self.worker_registry = worker_registry
        self.task_manager = task_manager

        self.worker_timeout = worker_timeout

    # ==================================================
    # RECEIVE HEARTBEAT
    # ==================================================

    def receive_heartbeat(
        self,
        worker_id: str
    ) -> bool:
        """
        Updates worker's last heartbeat.

        Called by API endpoint.

        Returns
        -------
        True if worker exists
        False otherwise
        """

        worker = self.worker_registry.get_worker(worker_id)

        if not worker:
            return False

        worker["last_heartbeat"] = datetime.utcnow()

        worker["status"] = "IDLE" \
            if worker.get("current_task") is None \
            else "BUSY"

        return True

    # ==================================================
    # CHECK SINGLE WORKER
    # ==================================================

    def is_worker_dead(
        self,
        worker_id: str
    ) -> bool:
        """
        Returns True if worker
        exceeded timeout.
        """

        worker = self.worker_registry.get_worker(worker_id)

        if not worker:
            return False

        last_heartbeat = worker.get("last_heartbeat")

        if not last_heartbeat:
            return True

        elapsed_seconds = (
            datetime.utcnow() - last_heartbeat
        ).total_seconds()

        return elapsed_seconds > self.worker_timeout

    # ==================================================
    # FIND DEAD WORKERS
    # ==================================================

    def get_dead_workers(self) -> List[str]:
        """
        Returns list of dead worker ids.
        """

        dead_workers = []

        workers = self.worker_registry.get_all_workers()

        for worker_id in workers:

            if self.is_worker_dead(worker_id):
                dead_workers.append(worker_id)

        return dead_workers

    # ==================================================
    # MARK WORKER DEAD
    # ==================================================

    def mark_worker_dead(
        self,
        worker_id: str
    ):
        """
        Updates worker status.

        Does not delete worker.

        Keeping dead workers helps
        debugging and monitoring.
        """

        worker = self.worker_registry.get_worker(worker_id)

        if not worker:
            return

        worker["status"] = "DEAD"

    # ==================================================
    # RECOVER TASKS
    # ==================================================

    def recover_worker_tasks(
        self,
        worker_id: str
    ):
        """
        Any task running on this worker
        must be reassigned.

        Flow:

        RUNNING
            ↓
        FAILED
            ↓
        PENDING
        """

        tasks = self.task_manager.get_all_tasks()

        for task in tasks.values():

            assigned_worker = task.get(
                "assigned_worker"
            )

            task_status = task.get("status")

            if (
                assigned_worker == worker_id
                and task_status == "RUNNING"
            ):

                self.task_manager.fail_task(
                    task["task_id"]
                )

                self.task_manager.retry_task(
                    task["task_id"]
                )

    # ==================================================
    # HANDLE DEAD WORKER
    # ==================================================

    def handle_worker_failure(
        self,
        worker_id: str
    ):
        """
        Complete failure workflow.
        """

        self.mark_worker_dead(worker_id)

        self.recover_worker_tasks(worker_id)

    # ==================================================
    # MAIN MONITORING LOOP
    # ==================================================

    def check_workers(self):
        """
        Called periodically.

        Example:

        Every 5 seconds.

        Detects dead workers and
        triggers recovery.
        """

        dead_workers = self.get_dead_workers()

        for worker_id in dead_workers:

            worker = self.worker_registry.get_worker(
                worker_id
            )

            if (
                worker
                and worker["status"] != "DEAD"
            ):
                self.handle_worker_failure(
                    worker_id
                )

    # ==================================================
    # WORKER HEALTH REPORT
    # ==================================================

    def get_worker_health_report(self):
        """
        Dashboard endpoint helper.
        """

        workers = self.worker_registry.get_all_workers()

        report = {
            "total_workers": 0,
            "healthy_workers": 0,
            "dead_workers": 0
        }

        report["total_workers"] = len(workers)

        for worker in workers.values():

            if worker["status"] == "DEAD":
                report["dead_workers"] += 1
            else:
                report["healthy_workers"] += 1

        return report

    # ==================================================
    # GET UNRESPONSIVE WORKERS
    # ==================================================

    def get_unresponsive_workers(self):
        """
        Useful for monitoring UI.
        """

        result = []

        workers = self.worker_registry.get_all_workers()

        for worker_id, worker in workers.items():

            last_seen = worker.get(
                "last_heartbeat"
            )

            if not last_seen:
                continue

            elapsed = (
                datetime.utcnow() - last_seen
            ).total_seconds()

            result.append({
                "worker_id": worker_id,
                "seconds_since_last_heartbeat":
                    round(elapsed, 2)
            })

        return sorted(
            result,
            key=lambda x:
            x["seconds_since_last_heartbeat"],
            reverse=True
        )