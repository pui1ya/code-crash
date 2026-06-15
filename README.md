# 🚀 CrashReduce

> A fault-tolerant MapReduce engine built from scratch in Python, inspired by Google's 2004 MapReduce paper and MIT 6.824 Distributed Systems.

CrashReduce is a distributed data processing framework that executes MapReduce jobs across multiple worker nodes while automatically recovering from worker failures.

The project demonstrates core distributed systems concepts including:

* Distributed task scheduling
* Worker registration and discovery
* Heartbeat monitoring
* Failure detection
* Task reassignment
* Fault tolerance
* Parallel data processing
* Cluster monitoring
* Performance benchmarking

---

# ✨ Features

## Distributed Execution

Run MapReduce workloads across multiple worker nodes simultaneously.

```text
Input Data
     ↓
Map Tasks
     ↓
Shuffle & Sort
     ↓
Reduce Tasks
     ↓
Final Output
```

---

## Fault Tolerance

CrashReduce automatically recovers from worker failures.

```text
Worker Crash
      ↓
Heartbeat Timeout
      ↓
Worker Marked Dead
      ↓
Task Reassigned
      ↓
Job Continues
```

Demonstration:

```bash
docker stop worker2
```

The coordinator detects the failure and reassigns unfinished tasks to healthy workers.

---

## Multiple Built-in Jobs

### Word Count

Counts word occurrences across large datasets.

Example:

```text
hello world
hello python
```

Output:

```json
{
  "hello": 2,
  "world": 1,
  "python": 1
}
```

---

### Inverted Index

Creates a search-engine-style index.

Output:

```json
{
  "ai": ["doc1", "doc2"],
  "python": ["doc3"]
}
```

---

### Distributed Grep

Performs parallel text search across partitions.

Example:

```bash
search "machine learning"
```

Output:

```text
wiki_part_4.txt:31 Machine learning is...
wiki_part_8.txt:95 Machine learning models...
```

---

# 🏗 Architecture

```text
                         ┌──────────────┐
                         │ Dashboard    │
                         └──────┬───────┘
                                │
                                ▼

                    ┌────────────────────┐
                    │ Coordinator         │
                    └─────┬───────┬──────┘
                          │       │
                          │       │
                          ▼       ▼

                 ┌────────────┐ ┌────────────┐
                 │ Worker 1   │ │ Worker 2   │
                 └────────────┘ └────────────┘

                          ▼
                 ┌────────────┐
                 │ Worker N   │
                 └────────────┘

                          ▼
                 Storage / Output
```

---

# 📂 Project Structure

```text
crashreduce/
│
├── coordinator/
├── worker/
├── jobs/
├── common/
├── dashboard/
├── storage/
├── benchmark/
├── monitoring/
├── docker/
├── tests/
└── README.md
```

---

# ⚙️ Tech Stack

| Component        | Technology     |
| ---------------- | -------------- |
| Language         | Python 3.12    |
| API Framework    | FastAPI        |
| Dashboard        | React + Vite   |
| Monitoring       | Prometheus     |
| Visualization    | Grafana        |
| Containerization | Docker         |
| Orchestration    | Docker Compose |
| Testing          | Pytest         |
| Data Format      | JSON           |

---

# 🚦 Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/crashreduce.git

cd crashreduce
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start Coordinator

```bash
python -m coordinator.main
```

---

## Start Worker

```bash
python -m worker.main
```

Start multiple workers in separate terminals.

---

# 🐳 Running with Docker

Build and start the cluster:

```bash
docker compose up --build
```

Services:

| Service     | Port |
| ----------- | ---- |
| Coordinator | 8000 |
| Dashboard   | 3000 |
| Grafana     | 3001 |
| Prometheus  | 9090 |

---

# 📊 Monitoring

Prometheus collects:

* Worker heartbeats
* Task throughput
* Job metrics
* Failure events

Grafana visualizes:

* Worker health
* Job progress
* Cluster utilization
* Recovery events

---

# 🔥 Fault Tolerance Demo

Start cluster:

```bash
docker compose up
```

Submit a job.

Kill a worker:

```bash
docker stop crashreduce-worker-2
```

Observe:

```text
Worker marked DEAD
Task reassigned
Job completed successfully
```

---

# 📈 Benchmarking

Datasets are stored in:

```text
benchmark/wikipedia/
```

Reports are generated in:

```text
benchmark/reports/
```

Metrics include:

* Execution Time
* Throughput
* Worker Utilization
* Failure Recovery Time
* Task Completion Rate

---

# 🧪 Testing

Run all tests:

```bash
pytest
```

Run individual suites:

```bash
pytest tests/test_map.py

pytest tests/test_reduce.py

pytest tests/test_scheduler.py

pytest tests/test_recovery.py
```

---

# 🎯 Learning Objectives

CrashReduce demonstrates:

* Distributed Systems
* MapReduce Architecture
* Fault Tolerance
* Scheduling Algorithms
* Cluster Coordination
* Monitoring & Observability
* Containerized Deployments

---

# 🚀 Future Improvements

* Dynamic worker scaling
* Kubernetes deployment
* Distributed filesystem
* Checkpoint-based recovery
* gRPC communication
* Streaming MapReduce
* Job priority scheduling
* Multi-cluster execution

---

# 📚 References

* Google MapReduce Paper (2004)
* MIT 6.824 Distributed Systems
* FastAPI Documentation
* Docker Documentation
* Prometheus Documentation
* Grafana Documentation

---

# 👩‍💻 Author

**Punya Shree S**

Aspiring AI Engineer | Data Analyst | Distributed Systems Enthusiast

Building projects that combine software engineering, data systems, and machine learning.
