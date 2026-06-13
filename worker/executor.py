
"""
CrashReduce Executor

Purpose
--------------------------------------------------

Actually executes MapReduce tasks.

Receives task descriptions from worker/main.py

Determines whether the task is:

1. MAP
2. REDUCE

Then delegates execution to:

mapper.py
reducer.py

--------------------------------------------------

Execution Flow

Task
  ↓
Executor
  ↓
MAP ? -------- YES ------> Mapper
  ↓ NO
Reducer
  ↓
Output File
  ↓
Return Output Path
"""

from pathlib import Path
from datetime import datetime

from worker.mapper import Mapper
from worker.reducer import Reducer


class Executor:
    """
    Main execution engine for worker node.
    """

    def __init__(self):

        self.mapper = Mapper()

        self.reducer = Reducer()

        self.output_directory = (
            Path("storage/output")
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==========================================
    # VALIDATE TASK
    # ==========================================

    def validate_task(
        self,
        task: dict
    ):
        """
        Ensures required fields exist.

        Raises:
            ValueError
        """

        required_fields = [
            "task_id",
            "task_type",
            "job_id"
        ]

        for field in required_fields:

            if field not in task:

                raise ValueError(
                    f"Missing field: {field}"
                )

    # ==========================================
    # EXECUTE TASK
    # ==========================================

    def execute(
        self,
        task: dict
    ) -> str:
        """
        Main execution entrypoint.

        Parameters
        ----------
        task : dict

        Returns
        -------
        output_file_path
        """

        self.validate_task(task)

        task_type = task["task_type"]

        start_time = datetime.utcnow()

        print(
            f"[EXECUTOR] Starting "
            f"{task_type} task "
            f"{task['task_id']}"
        )

        # -----------------------------
        # MAP TASK
        # -----------------------------

        if task_type == "MAP":

            output_path = self.execute_map(
                task
            )

        # -----------------------------
        # REDUCE TASK
        # -----------------------------

        elif task_type == "REDUCE":

            output_path = self.execute_reduce(
                task
            )

        else:

            raise ValueError(
                f"Unknown task type: {task_type}"
            )

        end_time = datetime.utcnow()

        duration = (
            end_time - start_time
        ).total_seconds()

        print(
            f"[EXECUTOR] Finished "
            f"{task['task_id']} "
            f"in {duration:.2f}s"
        )

        return str(output_path)

    # ==========================================
    # EXECUTE MAP TASK
    # ==========================================

    def execute_map(
        self,
        task: dict
    ) -> Path:
        """
        Executes mapper.

        Returns path of intermediate file.
        """

        print(
            f"[MAP] Executing "
            f"{task['task_id']}"
        )

        output_path = self.mapper.run(
            task
        )

        return output_path

    # ==========================================
    # EXECUTE REDUCE TASK
    # ==========================================

    def execute_reduce(
        self,
        task: dict
    ) -> Path:
        """
        Executes reducer.

        Returns final output path.
        """

        print(
            f"[REDUCE] Executing "
            f"{task['task_id']}"
        )

        output_path = self.reducer.run(
            task
        )

        return output_path

    # ==========================================
    # EXECUTION METADATA
    # ==========================================

    def build_execution_record(
        self,
        task: dict,
        output_path: str,
        duration: float
    ) -> dict:
        """
        Future use:

        Execution history

        Metrics

        Monitoring
        """

        return {
            "task_id": task["task_id"],

            "job_id": task["job_id"],

            "task_type": task["task_type"],

            "output_path": output_path,

            "duration_seconds": duration,

            "completed_at":
                datetime.utcnow().isoformat()
        }

    # ==========================================
    # CLEANUP
    # ==========================================

    def cleanup(
        self,
        task: dict
    ):
        """
        Future hook.

        Used for:

        temp file cleanup

        memory cleanup

        cache cleanup
        """

        print(
            f"[CLEANUP] "
            f"{task['task_id']}"
        )