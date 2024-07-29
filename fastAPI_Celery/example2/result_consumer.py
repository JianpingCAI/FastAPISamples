from celery.result import AsyncResult
from celery_config import app

# Assuming you have the task ID
task_id = "some-task-id-here"

# Create a result instance using the task ID
result = AsyncResult(task_id, app=app)

# Check if the task is ready and print the result
if result.ready():
    print("Task complete: ", result.get())
else:
    print("Task is still processing...")
