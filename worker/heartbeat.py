
"""
CrashReduce Worker Heartbeat Service

Purpose
--------------------------------------------------

Sends periodic heartbeats to coordinator.

The coordinator uses heartbeats to determine:

1. Worker is alive
2. Worker is healthy
3. Worker has not crashed

--------------------------------------------------

Worker
   ↓
HeartbeatSender Thread
   ↓
POST /workers/heartbeat
   ↓
Coordinator

--------------------------------------------------

Runs independently from task execution.

Even while executing a large MapReduce task,
heartbeats must continue.
"""

import threading
import time
import requests
from datetime import datetime


class HeartbeatSender(threading.Thread):
    """
    Background heartbeat service.

    Runs in its own thread.

    Example:

    Worker Main Thread
            +
    Heartbeat Thread
    """

    def __init__(
        self,
        worker_id: str,
        coordinator_url: str,
        heartbeat_interval: int = 5
    ):
        """
        Parameters
        ----------

        worker_id:
            Assigned by coordinator

        coordinator_url:
            Coordinator base URL

        heartbeat_interval:
            Seconds between heartbeats
        """

        super().__init__()

        self.worker_id = worker_id

        self.coordinator_url = coordinator_url

        self.heartbeat_interval = heartbeat_interval

        self.running = True

        # Thread exits automatically
        # when worker process exits.
        self.daemon = True

    # ==========================================
    # SEND SINGLE HEARTBEAT
    # ==========================================

    def send_heartbeat(self):
        """
        Sends one heartbeat request.

        Returns
        -------
        True on success
        False on failure
        """

        try:

            response = requests.post(
                f"{self.coordinator_url}"
                f"/workers/heartbeat",

                params={
                    "worker_id": self.worker_id
                },

                timeout=5
            )

            response.raise_for_status()

            return True

        except Exception as e:

            print(
                "[HEARTBEAT ERROR] "
                f"{e}"
            )

            return False

    # ==========================================
    # MAIN HEARTBEAT LOOP
    # ==========================================

    def run(self):
        """
        Thread entrypoint.

        Runs forever until stopped.
        """

        print(
            "[HEARTBEAT] "
            "Heartbeat service started"
        )

        while self.running:

            success = self.send_heartbeat()

            if success:

                print(
                    "[HEARTBEAT] "
                    f"{datetime.utcnow().isoformat()}"
                )

            time.sleep(
                self.heartbeat_interval
            )

    # ==========================================
    # STOP HEARTBEAT SERVICE
    # ==========================================

    def stop(self):
        """
        Gracefully stop heartbeat thread.
        """

        self.running = False

        print(
            "[HEARTBEAT] "
            "Stopping heartbeat service"
        )

    # ==========================================
    # UPDATE INTERVAL
    # ==========================================

    def update_interval(
        self,
        new_interval: int
    ):
        """
        Allows dynamic heartbeat tuning.
        """

        self.heartbeat_interval = new_interval

        print(
            "[HEARTBEAT] "
            f"Interval updated to "
            f"{new_interval}s"
        )

    # ==========================================
    # GET STATUS
    # ==========================================

    def get_status(self):
        """
        Useful for debugging
        and monitoring.
        """

        return {
            "worker_id": self.worker_id,

            "interval":
                self.heartbeat_interval,

            "running":
                self.running
        }