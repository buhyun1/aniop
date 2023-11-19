# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory contents into the container at /app/src
COPY src/ /app/src/

# Set the environment variable to ensure Python outputs all its text to the terminal without buffering it
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "./src/main.py"]