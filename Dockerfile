# Use the official Python runtime image
FROM python:alpine3.22 AS builder
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app

# Copy content
COPY ./app ./

# Upgrade pip
RUN pip install --upgrade pip 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

 