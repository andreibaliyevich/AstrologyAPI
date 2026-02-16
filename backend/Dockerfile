FROM python:3.12.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /usr/src/backend
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
