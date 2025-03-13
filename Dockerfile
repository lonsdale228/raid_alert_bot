FROM python:3.11.8-slim

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    build-essential \
    && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt


CMD ["python", "./main.py"]