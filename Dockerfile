# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt update
RUN apt install -y git
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "-m", "examples.chat_forever.openai"]

# - `FROM python:3.8-slim`: This line sets the base image to Python 3.8, which is a slim version of the official Python image.

# - `WORKDIR /app`: This sets the working directory within the container to `/app`.

# - `COPY . /app`: This copies the contents of your current directory (where the Dockerfile is located) into the `/app` directory of the container.

# - `RUN pip install --trusted-host pypi.python.org -r requirements.txt`: This installs any Python dependencies listed in a `requirements.txt` file. Make sure to create this file in your project directory if you have dependencies.

# - `EXPOSE 80`: This exposes port 80, which is typically used for HTTP traffic. You can modify this port if your Flask app uses a different port.

# - `ENV NAME World`: This sets an environment variable named `NAME` with the value "World." You can customize this environment variable as needed.

# - `CMD ["python", "app.py"]`: This specifies the command to run when the container starts. In this case, it runs the `app.py` script. You should replace `app.py` with the name of your Flask application file.

# Make sure you have a `requirements.txt` file with your Flask application's dependencies, and place this Dockerfile in the root of your Flask application directory. Then, you can build the Docker image using `docker build` and run your Flask app within a container.