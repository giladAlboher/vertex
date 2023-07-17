# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install the dependencies


# Copy the Python script to the working directory
COPY . .


# Create a volume for logs
VOLUME /app/logs

# Set the command to run the Python script
CMD ["python", "main.py"]
