FROM python:3.13.9-slim

RUN apt-get update && apt-get install -y tzdata

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt


CMD ["python", "./bot.py"]