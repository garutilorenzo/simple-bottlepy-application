# As Scrapy runs on Python, I choose the official Python 3 Docker image.
FROM python:3

# PGSQL
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Set the working directory to /usr/src/app.
WORKDIR /app/src
 
# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt ./
 
# Install Scrapy specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt\
    && rm -rf ./requirements.txt

RUN groupadd -g 1000 web
RUN useradd -d /app/src -s /bin/bash -g web -u 1000 web

USER web