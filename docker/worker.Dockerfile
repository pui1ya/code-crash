# ==================================================
# CrashReduce Worker Image
# ==================================================

# Lightweight Python runtime
FROM python:3.12-slim

# ==================================================
# Environment Variables
# ==================================================

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ==================================================
# Working Directory
# ==================================================

WORKDIR /app

# ==================================================
# Install Python Dependencies
# ==================================================

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ==================================================
# Copy Source Code
# ==================================================

COPY worker/ worker/
COPY common/ common/
COPY jobs/ jobs/

# Worker needs storage folders
COPY storage/ storage/

# ==================================================
# Runtime Configuration
# ==================================================

ENV COORDINATOR_URL=http://coordinator:8000

ENV WORKER_PORT=9001

# ==================================================
# Expose Worker Port
# ==================================================

EXPOSE 9001

# ==================================================
# Start Worker
# ==================================================

CMD [
    "python",
    "-m",
    "worker.main"
]