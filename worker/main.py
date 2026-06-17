
"""
CrashReduce Worker

Responsibilities
--------------------------------------------------

1. Register with coordinator
2. Start heartbeat thread
3. Poll for tasks
4. Execute tasks
5. Report results

Worker Lifecycle

START
  ↓
REGISTER
  ↓
HEARTBEAT LOOP
  ↓
WAIT FOR TASK
  ↓
EXECUTE
  ↓
REPORT RESULT
  ↓
WAIT FOR NEXT TASK
"""

import time
import socket
import requests

from worker.executor import Executor
from worker.heartbeat import HeartbeatSender


# ==================================================
# CONFIGURATION
# ==================================================

COORDINATOR_URL = "http://localhost:8000"

POLL_INTERVAL = 3


# ==================================================
# WORKER CLASS
# ==================================================

class Worker:
    """
    Main worker process.
    """

    def __init__(
        self,
        worker_name: str,
        host: str,
        port: int
    ):

        self.worker_name = worker_name

        self.host = host

        self.port = port

        self.worker_id = None

        self.executor = Executor()

        self.heartbeat_sender = None

    # ==============================================
    # REGISTER WITH COORDINATOR
    # ==============================================

    def register(self):
        """
        Registers worker with coordinator.

        Coordinator returns worker_id.
        """

        try:

            response = requests.post(
                f"{COORDINATOR_URL}/workers/register",
                params={
                    "worker_name": self.worker_name
                }
            )

            response.raise_for_status()

            data = response.json()

            self.worker_id = data["worker_id"]

            print(
                f"[REGISTERED] Worker ID = {self.worker_id}"
            )

        except Exception as e:

            print(
                f"[ERROR] Registration failed: {e}"
            )

            raise

    # ==============================================
    # START HEARTBEATS
    # ==============================================

    def start_heartbeat_service(self):
        """
        Starts background heartbeat thread.
        """

        self.heartbeat_sender = HeartbeatSender(
            worker_id=self.worker_id,
            coordinator_url=COORDINATOR_URL
        )

        self.heartbeat_sender.start()

        print(
            "[HEARTBEAT] Background service started"
        )

    # ==============================================
    # POLL FOR TASK
    # ==============================================

    def request_task(self):
        """
        Ask coordinator for work.

        Returns:
            task dictionary

        Returns None if no task exists.
        """

        try:

            response = requests.get(
                f"{COORDINATOR_URL}/workers/"
                f"{self.worker_id}/task"
            )

            if response.status_code == 204:

                return None

            response.raise_for_status()

            return response.json()

        except Exception as e:

            print(
                f"[ERROR] Task request failed: {e}"
            )

            return None

    # ==============================================
    # REPORT SUCCESS
    # ==============================================

    def report_success(
        self,
        task_id: str,
        output_path: str
    ):
        """
        Inform coordinator that task completed.
        """
        response = requests.post(
            f"{COORDINATOR_URL}/tasks/{task_id}/complete",
            json={
                "worker_id": self.worker_id,
                "output_path": output_path
            }
        )

        print("COMPLETE RESPONSE:", response.status_code)
        print(response.text)

        response.raise_for_status()

    # ==============================================
    # REPORT FAILURE
    # ==============================================

    def report_failure(
        self,
        task_id: str,
        error_message: str
    ):
        """
        Inform coordinator that task failed.
        """

        try:

            requests.post(
                f"{COORDINATOR_URL}/tasks/"
                f"{task_id}/failed",
                json={
                    "worker_id": self.worker_id,
                    "error": error_message
                }
            )

        except Exception as e:

            print(
                f"[ERROR] Failed to report failure: {e}"
            )

    # ==============================================
    # PROCESS TASK
    # ==============================================

    def process_task(
        self,
        task: dict
    ):

        task_id = task["task_id"]

        try:

            print(f"[TASK] Starting {task_id}")

            print("[DEBUG] About to execute task")

            output_path = self.executor.execute(
                task
            )

            print(
                f"[DEBUG] Executor returned: {output_path}"
            )

            print(
                "[DEBUG] Reporting success"
            )

            self.report_success(
                task_id,
                output_path
            )

            print(
                "[DEBUG] Success reported"
            )

            print(
                f"[SUCCESS] {task_id}"
            )

        except Exception as e:

            print(
                f"[FAILED] {task_id}"
            )

            print(
                f"[ERROR] {e}"
            )

            self.report_failure(
                task_id,
                str(e)
            )
    # def process_task(
    #     self,
    #     task: dict
    # ):
    #     """
    #     Executes task using Executor.
    #     """

    #     task_id = task["task_id"]

    #     try:

    #         print(
    #             f"[TASK] Starting {task_id}"
    #         )

    #         output_path = self.executor.execute(
    #             task
    #         )

    #         self.report_success(
    #             task_id,
    #             output_path
    #         )

    #         print(
    #             f"[SUCCESS] {task_id}"
    #         )

    #     except Exception as e:

    #         print(
    #             f"[FAILED] {task_id}"
    #         )

    #         self.report_failure(
    #             task_id,
    #             str(e)
    #         )

    # ==============================================
    # MAIN LOOP
    # ==============================================

    def run(self):
        """
        Worker event loop.
        """

        self.register()

        self.start_heartbeat_service()

        print(
            "[READY] Waiting for tasks..."
        )

        while True:

            task = self.request_task()

            print("\nDEBUG TASK RESPONSE:")
            print(task)
            print()

            if not task:
                time.sleep(2)
                continue

            if "task_id" not in task:
                print("[INFO] No task assigned")
                time.sleep(2)
                continue

            self.process_task(task)


# ==================================================
# APPLICATION ENTRYPOINT
# ==================================================

if __name__ == "__main__":

    hostname = socket.gethostname()

    worker = Worker(
        worker_name=f"worker-{hostname}",
        host="localhost",
        port=9001
    )

    worker.run()