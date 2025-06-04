# Stage 1: Base image with system dependencies
FROM python:3.10-slim AS base
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create user and group
RUN groupadd -r -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser

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
    git \
    openssh-client \
 && rm -rf /var/lib/apt/lists/*

# Stage 2: SSH Key and Dependencies
FROM base AS ssh-stage
# Copy SSH directory with proper permissions
COPY --chown=appuser:appuser .ssh /home/appuser/.ssh

# Secure SSH key
RUN chmod 700 /home/appuser/.ssh && \
    chmod 600 /home/appuser/.ssh/id_rsa && \
    ssh-keyscan github.com >> /home/appuser/.ssh/known_hosts


# Stage 3: Python Dependencies
FROM ssh-stage AS dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install debugpy

# Final Stage: Application Setup
FROM dependencies AS final
WORKDIR /app

# Copy application files
COPY . /app

# Create necessary directories and set permissions
RUN mkdir -p /app/var && \
    chown -R appuser:appuser /app /home/appuser/.ssh

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app

# Expose debugging and application ports
EXPOSE 5678 5000

# Entrypoint
CMD ["./entrypoint.sh"]