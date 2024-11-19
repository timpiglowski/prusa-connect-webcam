FROM python:3.9-slim

# Install system dependencies for OpenCV and video devices
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create a non-root user and add to video group
RUN groupadd -r camera && \
    useradd -r -g camera -G video camera && \
    chown -R camera:camera /app

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Switch to non-root user
USER camera

CMD ["python", "main.py"]
