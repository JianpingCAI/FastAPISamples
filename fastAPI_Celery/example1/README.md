# FastAPI + Celery[Redis]

## Key Concepts

- Broker: A message transport mechanism. Celery supports RabbitMQ, Redis, and other brokers.
- Worker: A process that executes tasks.
- Task: A unit of work which is created from function calls and is scheduled to run asynchronously.
- Producer: Code that sends messages to the broker to be executed by workers.

## Docker

- install Docker Desktop on Windows

  ```bash
  sudo apt update
  sudo apt install docker.io
  ```

## Intall and Run Redis in a Docker Container

```bash
docker pull redis
docker run --name my-redis-container -p 6379:6379 -d redis
```

## Install Celey[redis]

```bash
pip install fastapi[all] celery[redis] uvicorn
```

## Start the fastAPI server

```bash
cd 
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Start the Celery worker

```bash
cd tasks
celery -A worker.celery_app worker --loglevel=info
```

## Install and Run the Flower

Flower: a web-based tool for monitoring and managing tasks

```bash

pip install Flower
cd tasks

celery -A worker.celery_app flower
```
