# Base image:
FROM python:3.12.3

# Setting the working directory WITHIN the container
WORKDIR /app

# Copying the current directory contents inside the container /app
COPY . /app/


# Install dependencies (not necessary in this example)
RUN pip install --no-cache-dir -r requirements.txt


# Running the application (ORIGINAL CODE)
# ENTRYPOINT [ "python", "docker_demo/hello_docker.py" ]  

# Running the application
ENTRYPOINT ["python", "data_cleaner_app/cleaner_app_dock.py"]