# Use the official Python image
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN groupadd -r -g 1000 appuser && \
    useradd -m -r -u 1000 -g appuser appuser

ENV HOME=/home/appuser

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    postgresql-client \
    netcat-openbsd \
    redis-tools \
    curl iputils-ping \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install debugpy
EXPOSE 5678

# Copy the application code
COPY . /app

RUN mkdir -p /app/var
# Change ownership of the /app directory to 'appuser'
RUN chown -R appuser:appuser /app

# Switch to 'appuser'
USER appuser

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5050

# Start the application
CMD ["./entrypoint.sh"]
