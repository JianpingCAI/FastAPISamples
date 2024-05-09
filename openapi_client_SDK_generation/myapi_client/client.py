from jianping_api_client import ApiClient, Configuration
from jianping_api_client.api import items_api, users_api
from jianping_api_client.models import Item, User


# Setup API Client
config = Configuration(host="http://localhost:8000")
client = ApiClient(configuration=config)

# Item API Instance
items_api_instance = items_api.ItemsApi(api_client=client)

# User API Instance
users_api_instance = users_api.UsersApi(api_client=client)

# Create an Item
item = Item(name="Sample Item", description="A sample item", price=100.0, tax=10.0)
created_item = items_api_instance.create_item(item)

print(f"Created Item: {created_item}")

# Create a User
user = User(username="johndoe", email="john@example.com", full_name="John Doe")
created_user = users_api_instance.create_user(user)

print(f"Created User: {created_user}")
