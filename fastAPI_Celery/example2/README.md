
## Start Celery worker

```bash
celery -A celery_config worker --loglevel=info

```

## Run the task

```bash
python run_tasks.py 
```

## Install and Run the Flower

Flower: a web-based tool for monitoring and managing tasks

```bash

pip install Flower
cd tasks

celery -A celery_config flower
```
