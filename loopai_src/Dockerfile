# Stage 1: Base image with system dependencies
FROM python:3.10-slim AS base
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create the app user and groups. Adjust the docker group GID if needed.
RUN groupadd -r -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser && \
    groupadd -g 991 dockersock && \
    usermod -aG dockersock appuser && \
    # Create a docker group with GID 999 (change this if your host uses a different GID)
    groupadd -r -g 999 docker && \
    usermod -aG docker appuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    postgresql-client \
    netcat-openbsd \
    redis-tools \
    curl \
    iputils-ping \
    docker.io \
    git \
    openssh-client \
 && rm -rf /var/lib/apt/lists/*

# Stage 2: Python Dependencies
FROM base AS dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install debugpy grequests httpx gevent-websocket

# Stage 3: Application Setup
FROM dependencies AS final
WORKDIR /app

# Copy the entire application code
COPY . /app

# Create necessary directories and set proper ownership
RUN mkdir -p /app/var && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app

# Expose the required ports
EXPOSE 5678 5000

# Entrypoint
CMD ["./entrypoint.sh"]