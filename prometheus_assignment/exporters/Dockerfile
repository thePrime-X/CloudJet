# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the exporter script
COPY custom_exporter.py .

# Install dependencies
RUN pip install --no-cache-dir prometheus_client requests

# Expose the metrics port
EXPOSE 8000

# Run the exporter
CMD ["python", "custom_exporter.py"]
