# Notes

- background queue
- one-by-one
- dedicated queue worker(s)

```bash
pip install dash[diskcache]
pip install dash[celery]
```

## Redis

```bash
sudo service redis-server status
```

## Run Celery with Redis

```bash

celery -A example2:celery_app worker --loglevel=INFO --concurrency=2
python example2.py


celery -A example6:celery_app worker --loglevel=INFO --concurrency=2
python example6.py

```
