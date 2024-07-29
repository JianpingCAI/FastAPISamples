from celery import Celery

# Initialize Celery
app = Celery(
    "thumbnail_generator",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks"],
)

# Optional: configure Celery to serialize data as JSON
app.conf.update(
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
