# FastAPI + Celery[Redis]

### Part 1: Project Setup

First, ensure you have Python and Redis installed on your system. You will also need the `Pillow` library for image processing:

```bash
pip install celery redis pillow
```

### Part 2: Setting Up Celery with Redis

Create a new Python script named `celery_config.py`. This script will set up Celery with Redis as the broker and result backend:

```python
from celery import Celery

# Initialize Celery
app = Celery('thumbnail_generator',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['tasks'])

# Optional: configure Celery to serialize data as JSON
app.conf.update(
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
```

### Part 3: Defining the Task

Create a new Python script named `tasks.py`. This will include a task that downloads an image from a URL and generates a thumbnail:

```python
from celery_config import app
from PIL import Image
import requests
from io import BytesIO

@app.task
def create_thumbnail(url, size=(128, 128)):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.thumbnail(size)
    
    # Save or send your thumbnail somewhere here
    img.save(f'thumbnail-{url.split("/")[-1]}')  # Simple filename extraction from URL
    
    return f'Thumbnail created for {url}'
```

This task downloads an image using `requests`, processes it with `PIL` to create a thumbnail, and saves it locally.

### Part 4: Running the Celery Worker

Open your terminal and navigate to the directory containing your project files. Run the following command to start the Celery worker:

```bash
celery -A celery_config worker --loglevel=info
```

This command starts a Celery worker that listens for tasks to process.

### Part 5: Invoking the Task

You can invoke the task from any Python script. Create a file named `run_tasks.py` and add the following code to use the `create_thumbnail` task:

```python
from tasks import create_thumbnail

# Example image URL
url = "https://example.com/sample.jpg"

# Asynchronously call the create_thumbnail task
result = create_thumbnail.delay(url)

# Wait for the task to finish and get the result
print(result.get())
```

### Part 6: Monitoring and Results

After invoking the task, you should see output in the Celery worker's terminal indicating that the task was received and processed. The result of the task (confirmation of the thumbnail creation) will be printed by the `print(result.get())` call in `run_tasks.py`.

### Conclusion

This example covers the full workflow of setting up a Celery application with Redis, defining a task to process image URLs into thumbnails, running a Celery worker to handle tasks, and invoking the task from a Python script. This setup can be expanded or modified for more complex workflows, including handling errors, retrying tasks, and more.
