from dash import html
import requests

layout = html.Div([
    html.H2("Blogs"),
    html.Div(id='blog-list')
    # Additional content and components will be added here.
])

# This function will be connected to a callback to fetch blogs from the API
def fetch_blogs():
    response = requests.get('http://localhost:8000/blogs/')
    if response.status_code == 200:
        blogs = response.json()
        return html.Ul([html.Li(blog['title']) for blog in blogs])
    return html.P("Failed to load blogs")
