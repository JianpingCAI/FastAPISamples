from dash import html
import requests

layout = html.Div([
    html.H2("Post"),
    html.Div(id='post-content'),
    html.H3("Comments"),
    html.Div(id='comment-list')
])

# This function will be connected to a callback to fetch a post from the API
def fetch_post(post_id):
    response = requests.get(f'http://localhost:8000/posts/{post_id}')
    if response.status_code == 200:
        post = response.json()
        return html.Div([
            html.H4(post['title']),
            html.P(post['content'])
        ])
    return html.P("Failed to load post")

# This function will be connected to a callback to fetch comments from the API
def fetch_comments(post_id):
    response = requests.get(f'http://localhost:8000/posts/{post_id}/comments')
    if response.status_code == 200:
        comments = response.json()
        return html.Ul([html.Li(comment['content']) for comment in comments])
    return html.P("Failed to load comments")
