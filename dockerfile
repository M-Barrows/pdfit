# Dockerfile.dash
# This is the file for building the Docker image

# Use the official Python image as the base image
FROM python:3.10.13-slim-bullseye

# Set the environment variable for unbuffered output
ENV PYTHONUNBUFFERED 1
ENV FLASK_RUN_HOST=0.0.0.0

# Create a directory for the code and set it as the working directory
RUN mkdir /code
WORKDIR /code

# Copy the requirements file and install the dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the rest of the code into the image
EXPOSE 8080
COPY . /code/
CMD ["python", "app.py"]
