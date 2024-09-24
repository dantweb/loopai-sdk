# Use the official Python image
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -r -g 1000 appuser && useradd -r -u 1000 -g appuser appuser

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    postgresql-client \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Change ownership of the /app directory to 'appuser'
RUN chown -R appuser:appuser /app
RUN chown -R appuser:appuser /app/var

# Switch to 'appuser'
USER appuser

# Set environment variables
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Start the application
CMD ["./entrypoint.sh"]
