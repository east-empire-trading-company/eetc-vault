# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /eetc-vault

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy local code to the container image.
COPY . .

# Set environment variable FLASK_APP to main.py
ENV FLASK_APP=main.py

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to default value of 30(Workers silent for more than this many seconds are killed and restarted.).
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 30 main:app
