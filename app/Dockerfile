# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip to the latest version as root
RUN pip install --no-cache-dir --upgrade pip

# Create a new user 'appuser' and group 'appuser'
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory
WORKDIR /app

# Install build dependencies and clean up
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
COPY .. .

# Change ownership of the /app directory to 'appuser'
RUN chown -R appuser:appuser /app

# Switch to 'appuser'
USER appuser

# Copy the entrypoint script and set permissions
COPY ../entrypoint.sh /app/entrypoint.sh


# Expose the application's port
EXPOSE 5000

# Set the entrypoint to your script
ENTRYPOINT ["/app/entrypoint.sh"]
