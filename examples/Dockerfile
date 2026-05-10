# Dockerfile for CRAB Docker Compose Example
FROM python:3.12-slim

WORKDIR /app

# Copy the daemon and examples
COPY crab_daemon.py /app/
COPY examples/ /app/examples/

# CRAB is stdlib-only — no pip install needed

# Default: run the basic example
CMD ["python", "examples/basic.py"]
