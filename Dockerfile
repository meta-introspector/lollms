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


# Run app.py when the container launches
CMD ["python", "-m", "examples.chat_forever.openai","--host","0.0.0.0"]

