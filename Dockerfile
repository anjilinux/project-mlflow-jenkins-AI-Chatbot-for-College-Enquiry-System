# Use NVIDIA CUDA base image for GPU
FROM nvidia/cuda:13.1.1-cudnn-runtime-ubuntu24.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-full python3-venv python3-pip build-essential && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .
COPY model.pkl .
COPY vectorizer.pkl .

# Expose FastAPI port
EXPOSE 7777

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7777"]
