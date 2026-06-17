
"""
CrashReduce Task Manager

Responsible for:

1. Creating tasks
2. Tracking task state
3. Tracking retries
4. Tracking worker assignment
5. Managing Map and Reduce tasks
6. Reporting task statistics

The scheduler uses this component
to obtain pending tasks.

Workers never directly modify tasks.

Only the coordinator modifies task state.
"""

from datetime import datetime
from uuid import uuid4
from typing import Dict, List, Optional


class TaskManager:
    """
    Central task tracking component.
    """

    def __init__(self):

        # ------------------------------------------------
        # All tasks stored here
        #
        # key = task_id
        # value = task metadata
        # ------------------------------------------------

        self.tasks: Dict[str, dict] = {}

    # ==================================================
    # CREATE TASK
    # ==================================================

    def create_task(
        self,
        job_id: str,
        job_type: str,
        task_type: str,
        input_file: str,
        partition_id: int
    ) -> str:
        """
        Creates a new task.

        task_type:
            MAP
            REDUCE

        Returns:
            task_id
        """

        task_id = str(uuid4())

        self.tasks[task_id] = {
            "task_id": task_id,
            "job_id": job_id,
            "job_type": job_type,
            "task_type": task_type,
            "partition_id": partition_id,
            "input_file": input_file,

            "status": "PENDING",

            "assigned_worker": None,

            "retries": 0,

            "created_at": datetime.utcnow(),
            "started_at": None,
            "completed_at": None
        }

        return task_id

    # ==================================================
    # GET TASK
    # ==================================================

    def get_task(
        self,
        task_id: str
    ) -> Optional[dict]:
        """
        Returns task details.
        """

        return self.tasks.get(task_id)

    # ==================================================
    # GET ALL TASKS
    # ==================================================

    def get_all_tasks(self) -> Dict[str, dict]:
        """
        Returns all tasks.
        """

        return self.tasks

    # ==================================================
    # GET PENDING TASKS
    # ==================================================

    def get_pending_tasks(self) -> List[dict]:
        """
        Returns all pending tasks.
        """

        return [
            task
            for task in self.tasks.values()
            if task["status"] == "PENDING"
        ]

    # ==================================================
    # GET RUNNING TASKS
    # ==================================================

    def get_running_tasks(self) -> List[dict]:
        """
        Returns all running tasks.
        """

        return [
            task
            for task in self.tasks.values()
            if task["status"] == "RUNNING"
        ]

    # ==================================================
    # GET COMPLETED TASKS
    # ==================================================

    def get_completed_tasks(self) -> List[dict]:
        """
        Returns all completed tasks.
        """

        return [
            task
            for task in self.tasks.values()
            if task["status"] == "COMPLETED"
        ]

    # ==================================================
    # ASSIGN TASK TO WORKER
    # ==================================================

    def assign_task(
        self,
        task_id: str,
        worker_id: str
    ):
        """
        Called by scheduler.
        """

        if task_id not in self.tasks:
            return

        self.tasks[task_id]["assigned_worker"] = worker_id

        self.tasks[task_id]["status"] = "RUNNING"

        self.tasks[task_id]["started_at"] = datetime.utcnow()

    # ==================================================
    # COMPLETE TASK
    # ==================================================

    def complete_task(
        self,
        task_id: str
    ):
        """
        Called when worker finishes task.
        """

        if task_id not in self.tasks:
            return

        self.tasks[task_id]["status"] = "COMPLETED"

        self.tasks[task_id]["completed_at"] = datetime.utcnow()

    # ==================================================
    # FAIL TASK
    # ==================================================

    def fail_task(
        self,
        task_id: str
    ):
        """
        Called when:

        - worker crashes
        - timeout occurs
        - execution fails
        """

        if task_id not in self.tasks:
            return

        self.tasks[task_id]["status"] = "FAILED"

    # ==================================================
    # RETRY TASK
    # ==================================================

    def retry_task(
        self,
        task_id: str
    ):
        """
        Makes task eligible for reassignment.
        """

        if task_id not in self.tasks:
            return

        retries = self.tasks[task_id]["retries"]

        self.tasks[task_id]["retries"] = retries + 1

        self.tasks[task_id]["status"] = "PENDING"

        self.tasks[task_id]["assigned_worker"] = None

    # ==================================================
    # GET TASKS FOR JOB
    # ==================================================

    def get_tasks_by_job(
        self,
        job_id: str
    ) -> List[dict]:
        """
        Returns all tasks belonging
        to a specific job.
        """

        return [
            task
            for task in self.tasks.values()
            if task["job_id"] == job_id
        ]

    # ==================================================
    # CHECK MAP PHASE COMPLETE
    # ==================================================

    def map_phase_completed(
        self,
        job_id: str
    ) -> bool:
        """
        Used by Job Manager.

        Reduce phase cannot start
        until every map task finishes.
        """

        map_tasks = [
            task
            for task in self.tasks.values()
            if task["job_id"] == job_id
            and task["task_type"] == "MAP"
        ]

        if not map_tasks:
            return False

        return all(
            task["status"] == "COMPLETED"
            for task in map_tasks
        )

    # ==================================================
    # CHECK REDUCE PHASE COMPLETE
    # ==================================================

    def reduce_phase_completed(
        self,
        job_id: str
    ) -> bool:
        """
        Determines whether
        entire job is complete.
        """

        reduce_tasks = [
            task
            for task in self.tasks.values()
            if task["job_id"] == job_id
            and task["task_type"] == "REDUCE"
        ]

        if not reduce_tasks:
            return False

        return all(
            task["status"] == "COMPLETED"
            for task in reduce_tasks
        )

    # ==================================================
    # DELETE TASK
    # ==================================================

    def delete_task(
        self,
        task_id: str
    ):
        """
        Remove task completely.
        """

        if task_id in self.tasks:
            del self.tasks[task_id]

    # ==================================================
    # TASK SUMMARY
    # ==================================================

    def get_summary(self) -> dict:
        """
        Dashboard statistics.
        """

        pending = 0
        running = 0
        completed = 0
        failed = 0

        for task in self.tasks.values():

            status = task["status"]

            if status == "PENDING":
                pending += 1

            elif status == "RUNNING":
                running += 1

            elif status == "COMPLETED":
                completed += 1

            elif status == "FAILED":
                failed += 1

        return {
            "total_tasks": len(self.tasks),
            "pending_tasks": pending,
            "running_tasks": running,
            "completed_tasks": completed,
            "failed_tasks": failed
        }