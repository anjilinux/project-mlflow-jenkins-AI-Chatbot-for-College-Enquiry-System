FROM nvidia/cuda:13.1.1-cudnn-runtime-ubuntu24.04

WORKDIR /app

# Python installation
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
COPY model.pkl .
COPY vectorizer.pkl .

EXPOSE 7777

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7777"]
