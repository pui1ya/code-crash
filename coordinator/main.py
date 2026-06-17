
"""
CrashReduce Coordinator

This is the central coordinator (master node) of the MapReduce system.

Responsibilities:
---------------------------------------------------
1. Accept worker registrations
2. Receive worker heartbeats
3. Accept new jobs
4. Expose monitoring endpoints
5. Maintain cluster state

NOTE:
This file should only contain API endpoints and
server startup logic.

Business logic should be delegated to:

worker_registry.py
heartbeat_monitor.py
job_manager.py
scheduler.py
"""

from fastapi import FastAPI
from fastapi import HTTPException
from datetime import datetime
from uuid import uuid4
from coordinator.task_manager import TaskManager

# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="CrashReduce Coordinator",
    version="1.0.0",
    description="Fault Tolerant MapReduce Coordinator"
)

# =====================================================
# Temporary In-Memory State
#
# Later these will move to:
#
# worker_registry.py
# job_manager.py
#
# Keeping them here initially helps us test APIs
# before implementing the actual modules.
# =====================================================

workers = {}
tasks = {}
jobs = {}
task_manager = TaskManager()

# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health_check():
    """
    Used by:
    - Docker
    - Monitoring tools
    - Developers

    Verifies coordinator is alive.
    """

    return {
        "status": "healthy",
        "service": "coordinator",
        "timestamp": datetime.utcnow()
    }


# =====================================================
# WORKER REGISTRATION
# =====================================================

@app.post("/workers/register")
def register_worker(worker_name: str):
    """
    Called when a worker starts.

    Example:
    Worker boots up
          ↓
    Registers itself
          ↓
    Coordinator stores worker info
    """

    worker_id = str(uuid4())

    workers[worker_id] = {
        "worker_id": worker_id,
        "worker_name": worker_name,
        "status": "IDLE",
        "last_heartbeat": datetime.utcnow(),
        "registered_at": datetime.utcnow()
    }

    return {
        "message": "Worker registered successfully",
        "worker_id": worker_id
    }


# =====================================================
# HEARTBEATS
# =====================================================

@app.post("/workers/heartbeat")
def worker_heartbeat(worker_id: str):
    """
    Called every few seconds by workers.

    Example:

    Worker
      ↓
    POST heartbeat
      ↓
    Coordinator updates timestamp
    """

    if worker_id not in workers:
        raise HTTPException(
            status_code=404,
            detail="Worker not found"
        )

    workers[worker_id]["last_heartbeat"] = datetime.utcnow()

    return {
        "message": "Heartbeat received"
    }


# =====================================================
# LIST WORKERS
# =====================================================

@app.get("/workers")
def get_workers():
    """
    Monitoring endpoint.

    Dashboard uses this endpoint
    to display all workers.
    """

    return {
        "total_workers": len(workers),
        "workers": workers
    }


# =====================================================
# JOB SUBMISSION
# =====================================================

@app.post("/jobs/submit")
def submit_job(
    job_type: str,
    input_file: str
):
    """
    Submits a MapReduce job.

    Examples:

    WordCount

    InvertedIndex

    Grep

    The scheduler will later pick
    tasks from this job.
    """

    job_id = str(uuid4())

    jobs[job_id] = {
    "job_id": job_id,
    "job_type": job_type,
    "input_file": input_file,
    "status": "PENDING",
    "submitted_at": datetime.utcnow()
    }

    task_id = task_manager.create_task(
    job_id=job_id,
    job_type=job_type,
    task_type="MAP",
    input_file=input_file,
    partition_id=0
    )
    print("========== DEBUG ==========")
    print("JOB CREATED:", job_id)
    print("TASK CREATED:", task_id)
    print("TASK COUNT:", len(task_manager.tasks))
    print("ALL TASKS:", task_manager.tasks)
    print("===========================")

    return {
        "message": "Job submitted",
        "job_id": job_id,
        "task_id": task_id
    }


# =====================================================
# LIST JOBS
# =====================================================

@app.get("/jobs")
def get_jobs():
    """
    Returns all submitted jobs.

    Useful for dashboard.
    """

    return {
        "total_jobs": len(jobs),
        "jobs": jobs
    }


# =====================================================
# JOB DETAILS
# =====================================================

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    """
    Returns details of a single job.
    """

    if job_id not in jobs:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return jobs[job_id]

from fastapi import Response

@app.get("/workers/{worker_id}/task")
def get_task(worker_id: str):

    pending_tasks = task_manager.get_pending_tasks()

    if not pending_tasks:
        return {
            "message": "No tasks available"
        }

    task = pending_tasks[0]

    task_manager.assign_task(
        task["task_id"],
        worker_id
    )

    return task_manager.get_task(
        task["task_id"]
    )

# =====================================================
# ROOT ROUTE
# =====================================================

@app.get("/")
def root():
    """
    Simple welcome endpoint.
    """

    return {
        "message": "Welcome to CrashReduce Coordinator"
    }

@app.get("/tasks")
def get_tasks():
    print("GET TASKS CALLED")
    print("TASK COUNT:", len(task_manager.tasks))
    return task_manager.get_all_tasks()

@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: str):

    task = task_manager.get_task(task_id)

    if not task:
        return {
            "error": "Task not found"
        }

    task_manager.complete_task(task_id)

    if task["task_type"] == "MAP":

        reduce_task_id = task_manager.create_task(
            job_id=task["job_id"],
            job_type=task["job_type"],
            task_type="REDUCE",
            input_file="",
            partition_id=0
        )

        print(
            f"[REDUCE CREATED] {reduce_task_id}"
        )

    elif task["task_type"] == "REDUCE":

        jobs[task["job_id"]]["status"] = (
            "COMPLETED"
        )

        print(
            f"[JOB COMPLETED] "
            f"{task['job_id']}"
        )

    return {
        "message": "Task completed",
        "task_id": task_id
    }

@app.post("/tasks/{task_id}/failed")
def fail_task(task_id: str):

    task = task_manager.get_task(task_id)

    if not task:
        return {"error": "Task not found"}

    task_manager.fail_task(task_id)

    return {
        "message": "Task marked failed",
        "task_id": task_id
    }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):

    task_manager.delete_task(task_id)

    return {
        "message": "Task deleted"
    }

# =====================================================
# SERVER STARTUP
# =====================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
