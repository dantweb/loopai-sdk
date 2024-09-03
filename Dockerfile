# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=web.web_interface.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
