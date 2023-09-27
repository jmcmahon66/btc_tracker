# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

RUN mkdir Main

# Copy files into the container
COPY requirements.txt /app
COPY Main/tracker.py /app/Main
COPY Fonts/ /app

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to the tracker script
CMD ["python", "Main/tracker.py"]
