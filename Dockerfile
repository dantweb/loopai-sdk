# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

# Create a non-root user and group
RUN addgroup --system appuser && adduser --system --ingroup appuser appuser

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container
COPY . .

# Ensure that the log file exists and has the correct permissions
RUN touch /app/app.log && chown appuser:appuser /app/app.log

# Change ownership of the app directory to the appuser
RUN chown -R appuser:appuser /app

# Expose the port that the app runs on
EXPOSE 5000

# Switch to the non-root user
USER appuser

# Define environment variable for Flask
ENV FLASK_APP=web.web_interface.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
