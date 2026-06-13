# ==================================================
# CrashReduce Coordinator Image
# ==================================================

# Use lightweight Python image
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
# Install Dependencies
# ==================================================

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ==================================================
# Copy Project Files
# ==================================================

COPY coordinator/ coordinator/
COPY common/ common/
COPY jobs/ jobs/

# Optional if coordinator accesses storage
COPY storage/ storage/

# ==================================================
# Expose Coordinator Port
# ==================================================

EXPOSE 8000

# ==================================================
# Start Coordinator
# ==================================================

CMD [
    "uvicorn",
    "coordinator.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000"
]