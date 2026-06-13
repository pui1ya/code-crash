
/*
====================================================
CrashReduce Database Schema
====================================================

Target Database:

PostgreSQL

Purpose:

Persist:

- Workers
- Jobs
- Tasks
- Heartbeats
- Recovery Events

====================================================
*/


-- ==================================================
-- WORKERS
-- ==================================================

CREATE TABLE workers (

    worker_id VARCHAR(100)
        PRIMARY KEY,

    worker_name VARCHAR(255)
        NOT NULL,

    host VARCHAR(255)
        NOT NULL,

    port INTEGER
        NOT NULL,

    status VARCHAR(50)
        NOT NULL,

    current_task VARCHAR(100),

    tasks_completed INTEGER
        DEFAULT 0,

    tasks_failed INTEGER
        DEFAULT 0,

    registered_at TIMESTAMP
        NOT NULL,

    last_heartbeat TIMESTAMP
        NOT NULL
);


-- ==================================================
-- JOBS
-- ==================================================

CREATE TABLE jobs (

    job_id VARCHAR(100)
        PRIMARY KEY,

    job_type VARCHAR(100)
        NOT NULL,

    input_file TEXT
        NOT NULL,

    status VARCHAR(50)
        NOT NULL,

    map_partitions INTEGER
        NOT NULL,

    reduce_partitions INTEGER
        NOT NULL,

    progress_percentage NUMERIC(5,2)
        DEFAULT 0,

    created_at TIMESTAMP
        NOT NULL,

    completed_at TIMESTAMP
);


-- ==================================================
-- TASKS
-- ==================================================

CREATE TABLE tasks (

    task_id VARCHAR(100)
        PRIMARY KEY,

    job_id VARCHAR(100)
        NOT NULL,

    assigned_worker VARCHAR(100),

    task_type VARCHAR(50)
        NOT NULL,

    job_type VARCHAR(100)
        NOT NULL,

    partition_id INTEGER
        NOT NULL,

    input_file TEXT
        NOT NULL,

    status VARCHAR(50)
        NOT NULL,

    retries INTEGER
        DEFAULT 0,

    created_at TIMESTAMP
        NOT NULL,

    started_at TIMESTAMP,

    completed_at TIMESTAMP,

    CONSTRAINT fk_tasks_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_tasks_worker
        FOREIGN KEY (assigned_worker)
        REFERENCES workers(worker_id)
        ON DELETE SET NULL
);


-- ==================================================
-- HEARTBEATS
-- ==================================================

CREATE TABLE heartbeats (

    heartbeat_id BIGSERIAL
        PRIMARY KEY,

    worker_id VARCHAR(100)
        NOT NULL,

    heartbeat_timestamp TIMESTAMP
        NOT NULL,

    status VARCHAR(50)
        DEFAULT 'ALIVE',

    CONSTRAINT fk_heartbeat_worker
        FOREIGN KEY (worker_id)
        REFERENCES workers(worker_id)
        ON DELETE CASCADE
);


-- ==================================================
-- TASK RESULTS
-- ==================================================

CREATE TABLE task_results (

    result_id BIGSERIAL
        PRIMARY KEY,

    task_id VARCHAR(100)
        NOT NULL,

    worker_id VARCHAR(100)
        NOT NULL,

    output_path TEXT
        NOT NULL,

    execution_time_seconds NUMERIC(10,2),

    completed_at TIMESTAMP
        NOT NULL,

    CONSTRAINT fk_result_task
        FOREIGN KEY (task_id)
        REFERENCES tasks(task_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_result_worker
        FOREIGN KEY (worker_id)
        REFERENCES workers(worker_id)
        ON DELETE CASCADE
);


-- ==================================================
-- TASK FAILURES
-- ==================================================

CREATE TABLE task_failures (

    failure_id BIGSERIAL
        PRIMARY KEY,

    task_id VARCHAR(100)
        NOT NULL,

    worker_id VARCHAR(100),

    error_message TEXT,

    failed_at TIMESTAMP
        NOT NULL,

    CONSTRAINT fk_failure_task
        FOREIGN KEY (task_id)
        REFERENCES tasks(task_id)
        ON DELETE CASCADE
);


-- ==================================================
-- RECOVERY EVENTS
-- ==================================================

CREATE TABLE recovery_events (

    recovery_id BIGSERIAL
        PRIMARY KEY,

    worker_id VARCHAR(100)
        NOT NULL,

    task_id VARCHAR(100)
        NOT NULL,

    recovery_reason TEXT
        NOT NULL,

    recovered_at TIMESTAMP
        NOT NULL,

    CONSTRAINT fk_recovery_worker
        FOREIGN KEY (worker_id)
        REFERENCES workers(worker_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_recovery_task
        FOREIGN KEY (task_id)
        REFERENCES tasks(task_id)
        ON DELETE CASCADE
);


-- ==================================================
-- JOB METRICS
-- ==================================================

CREATE TABLE job_metrics (

    metric_id BIGSERIAL
        PRIMARY KEY,

    job_id VARCHAR(100)
        NOT NULL,

    total_tasks INTEGER
        NOT NULL,

    completed_tasks INTEGER
        NOT NULL,

    failed_tasks INTEGER
        DEFAULT 0,

    execution_time_seconds NUMERIC(12,2),

    created_at TIMESTAMP
        NOT NULL,

    CONSTRAINT fk_metrics_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE
);


-- ==================================================
-- INDEXES
-- ==================================================

CREATE INDEX idx_tasks_status
ON tasks(status);

CREATE INDEX idx_tasks_job
ON tasks(job_id);

CREATE INDEX idx_tasks_worker
ON tasks(assigned_worker);

CREATE INDEX idx_workers_status
ON workers(status);

CREATE INDEX idx_jobs_status
ON jobs(status);

CREATE INDEX idx_heartbeats_worker
ON heartbeats(worker_id);

CREATE INDEX idx_heartbeats_timestamp
ON heartbeats(heartbeat_timestamp);

CREATE INDEX idx_recovery_worker
ON recovery_events(worker_id);

CREATE INDEX idx_recovery_task
ON recovery_events(task_id);

