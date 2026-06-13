
"""
CrashReduce Job Manager

Responsible for:

1. Creating jobs
2. Splitting input files
3. Creating MAP tasks
4. Monitoring MAP phase
5. Creating REDUCE tasks
6. Marking jobs complete
7. Reporting progress

----------------------------------------------------

Job Lifecycle

SUBMITTED
    ↓
MAP_PHASE
    ↓
MAP_COMPLETE
    ↓
REDUCE_PHASE
    ↓
REDUCE_COMPLETE
    ↓
COMPLETED
"""

from uuid import uuid4
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class JobManager:
    """
    Central job tracking component.

    Depends on:

    - TaskManager
    """

    def __init__(
        self,
        task_manager,
        map_partitions: int = 4,
        reduce_partitions: int = 2
    ):
        self.task_manager = task_manager

        self.map_partitions = map_partitions

        self.reduce_partitions = reduce_partitions

        self.jobs: Dict[str, dict] = {}

    # ==================================================
    # CREATE JOB
    # ==================================================

    def create_job(
        self,
        job_type: str,
        input_file: str
    ) -> str:
        """
        Creates a new job.

        Example:

        WordCount
        InvertedIndex
        Grep
        """

        job_id = str(uuid4())

        self.jobs[job_id] = {
            "job_id": job_id,

            "job_type": job_type,

            "input_file": input_file,

            "status": "SUBMITTED",

            "map_partitions":
                self.map_partitions,

            "reduce_partitions":
                self.reduce_partitions,

            "created_at":
                datetime.utcnow(),

            "completed_at":
                None
        }

        return job_id

    # ==================================================
    # GET JOB
    # ==================================================

    def get_job(
        self,
        job_id: str
    ) -> Optional[dict]:
        """
        Returns job metadata.
        """

        return self.jobs.get(job_id)

    # ==================================================
    # GET ALL JOBS
    # ==================================================

    def get_all_jobs(self):
        """
        Returns all jobs.
        """

        return self.jobs

    # ==================================================
    # SPLIT INPUT FILE
    # ==================================================

    def split_input_file(
        self,
        input_file: str
    ):
        """
        Simulates file partitioning.

        In a real implementation,
        this would physically split
        a large file into chunks.

        Example:

        wiki.xml

        becomes

        wiki_part_0
        wiki_part_1
        wiki_part_2
        wiki_part_3
        """

        partitions = []

        for partition_id in range(
            self.map_partitions
        ):
            partitions.append(
                f"{input_file}_part_{partition_id}"
            )

        return partitions

    # ==================================================
    # CREATE MAP TASKS
    # ==================================================

    def create_map_tasks(
        self,
        job_id: str
    ):
        """
        Creates MAP tasks
        for the job.
        """

        job = self.get_job(job_id)

        if not job:
            return

        partitions = self.split_input_file(
            job["input_file"]
        )

        for partition_id, partition_file in enumerate(
            partitions
        ):

            self.task_manager.create_task(
                job_id=job_id,
                task_type="MAP",
                input_file=partition_file,
                partition_id=partition_id
            )

        job["status"] = "MAP_PHASE"

    # ==================================================
    # CHECK MAP PHASE
    # ==================================================

    def check_map_phase(
        self,
        job_id: str
    ) -> bool:
        """
        Returns True when all
        map tasks complete.
        """

        return self.task_manager.map_phase_completed(
            job_id
        )

    # ==================================================
    # CREATE REDUCE TASKS
    # ==================================================

    def create_reduce_tasks(
        self,
        job_id: str
    ):
        """
        Creates REDUCE tasks.

        Called only after
        all MAP tasks finish.
        """

        job = self.get_job(job_id)

        if not job:
            return

        for reduce_partition in range(
            self.reduce_partitions
        ):

            self.task_manager.create_task(
                job_id=job_id,

                task_type="REDUCE",

                input_file=f"reduce_partition_{reduce_partition}",

                partition_id=reduce_partition
            )

        job["status"] = "REDUCE_PHASE"

    # ==================================================
    # CHECK REDUCE PHASE
    # ==================================================

    def check_reduce_phase(
        self,
        job_id: str
    ) -> bool:
        """
        Returns True when all
        reduce tasks complete.
        """

        return self.task_manager.reduce_phase_completed(
            job_id
        )

    # ==================================================
    # COMPLETE JOB
    # ==================================================

    def complete_job(
        self,
        job_id: str
    ):
        """
        Mark job complete.
        """

        job = self.get_job(job_id)

        if not job:
            return

        job["status"] = "COMPLETED"

        job["completed_at"] = datetime.utcnow()

    # ==================================================
    # FAIL JOB
    # ==================================================

    def fail_job(
        self,
        job_id: str
    ):
        """
        Mark job failed.
        """

        job = self.get_job(job_id)

        if not job:
            return

        job["status"] = "FAILED"

    # ==================================================
    # UPDATE JOB STATE
    # ==================================================

    def update_job_state(
        self,
        job_id: str
    ):
        """
        Main orchestration method.

        Called periodically.

        Determines if job
        should advance to the
        next phase.
        """

        job = self.get_job(job_id)

        if not job:
            return

        current_status = job["status"]

        # ---------------------------
        # MAP PHASE COMPLETE
        # ---------------------------

        if current_status == "MAP_PHASE":

            if self.check_map_phase(job_id):

                job["status"] = "MAP_COMPLETE"

                self.create_reduce_tasks(job_id)

        # ---------------------------
        # REDUCE PHASE COMPLETE
        # ---------------------------

        elif current_status == "REDUCE_PHASE":

            if self.check_reduce_phase(job_id):

                job["status"] = "REDUCE_COMPLETE"

                self.complete_job(job_id)

    # ==================================================
    # JOB PROGRESS
    # ==================================================

    def get_job_progress(
        self,
        job_id: str
    ):
        """
        Returns progress metrics.
        """

        tasks = self.task_manager.get_tasks_by_job(
            job_id
        )

        total_tasks = len(tasks)

        if total_tasks == 0:
            return {
                "progress": 0
            }

        completed_tasks = len([
            task
            for task in tasks
            if task["status"] == "COMPLETED"
        ])

        progress = (
            completed_tasks
            / total_tasks
        ) * 100

        return {
            "job_id": job_id,

            "total_tasks": total_tasks,

            "completed_tasks":
                completed_tasks,

            "progress":
                round(progress, 2)
        }

    # ==================================================
    # JOB SUMMARY
    # ==================================================

    def get_summary(self):
        """
        Dashboard statistics.
        """

        completed = 0
        running = 0
        failed = 0

        for job in self.jobs.values():

            status = job["status"]

            if status == "COMPLETED":
                completed += 1

            elif status == "FAILED":
                failed += 1

            else:
                running += 1

        return {
            "total_jobs": len(self.jobs),

            "running_jobs": running,

            "completed_jobs": completed,

            "failed_jobs": failed
        }
