FROM python:3.12-slim

# Install required packages
RUN pip install --no-cache-dir requests

# Set working directory
WORKDIR /app

# Copy the poller script
COPY poller.py /app/poller.py

# Set environment variables (optional for runtime flexibility)
ENV GITHUB_API_URL="" \
    GITHUB_TOKEN="" \
    LAST_COMMIT_FILE="/data/last_commit.txt" \
    ARGO_EVENT_SOURCE_URL=""

# Create data directory
RUN mkdir -p /data

# Run the script
CMD ["python", "/app/poller.py"]
