from celery import Celery, current_task
import time


# Configure Celery
celery_app = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


@celery_app.task(bind=True)
def long_running_task(self, x):
    try:
        total = x
        for i in range(total):
            time.sleep(1)
            if i == 5:
                raise ValueError("Example error at iteration 5")
            self.update_state(state="PROGRESS", meta={"current": i, "total": total})
        return f"Task completed after processing {total} items"
    except Exception as e:
        self.update_state(
            state="FAILURE", meta={"exc_type": type(e).__name__, "exc_message": str(e)}
        )
        raise e
