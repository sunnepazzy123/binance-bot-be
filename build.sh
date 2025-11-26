#!/bin/bash

# Build Docker image with the specified tag
docker build -t vibratewarsaw/darkmind-bot-be .

# Optional: You can add error handling or messages
if [ $? -eq 0 ]; then
  echo "Docker image built successfully!"
else
  echo "Error occurred while building the Docker image."
  exit 1
fi

docker push vibratewarsaw/darkmind-bot-be:latest

# Optional: You can add error handling or messages
if [ $? -eq 0 ]; then
  echo "Docker image pushed to docker hub successfully!"
else
  echo "Error occurred while pushing the Docker image."
  exit 1
fi
