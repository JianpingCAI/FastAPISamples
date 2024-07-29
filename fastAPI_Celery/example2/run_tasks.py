from tasks import create_thumbnail

# Example image URL
url = "https://picsum.photos/200/300.jpg"

# Asynchronously call the create_thumbnail task
result = create_thumbnail.delay(url)

# Wait for the task to finish and get the result
print(result.get())
