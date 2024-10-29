# Use the official Python image from the Docker Hub
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    && pip install --no-cache-dir boto3

# Set the working directory in the container
WORKDIR /app

COPY ./order_processing.py /app

# Run products_lookup.py when the container launches
CMD ["python", "order_processing.py"]