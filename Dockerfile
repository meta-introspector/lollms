# Use an official Python runtime as a parent image
#FROM ai_ticket
ARG BASE_IMAGE
FROM ${BASE_IMAGE} 

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN apt update
RUN apt install -y git
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app/
# Run app.py when the container launches
CMD ["python", "-m", "lollms.apps.elf","--host","0.0.0.0"]

