# Base image:
FROM python:3.12.3

# Setting the working directory WITHIN the container
WORKDIR /app

# Copying the current directory contents inside the container /app
COPY . /app/

# Install dependencies (not necessary in this example)

# Running the application 
ENTRYPOINT [ "python", "docker_demo/hello_docker.py" ]