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

## Start the Celery worker

```bash
celery -A worker.celery_app worker --loglevel=info
```
