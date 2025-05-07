# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# Copy app directory, run.py, and config.py
COPY app/ ./app/
COPY run.py .
COPY config.py .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (optional, can be set in config.py or via docker run)
# ENV FLASK_APP=run.py # Not needed if using 'flask run' as below
# ENV FLASK_ENV=production # Or development

# Run run.py when the container launches
# Use 0.0.0.0 to make it accessible from outside the container
CMD ["flask", "run", "--host=0.0.0.0"]
