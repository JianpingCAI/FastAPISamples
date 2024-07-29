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

    return f"Thumbnail created for {url}"
