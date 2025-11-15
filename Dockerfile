FROM python:3.13.9-slim

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt


CMD ["python", "./bot.py"]