from dash import html
import requests

layout = html.Div([
    html.H2("User Profile"),
    html.Div(id='user-profile')
])

# This function will be connected to a callback to fetch user data from the API
def fetch_user(user_id):
    response = requests.get(f'http://localhost:8000/users/{user_id}')
    if response.status_code == 200:
        user = response.json()
        return html.Div([
            html.H3(user['username']),
            html.P(f"Email: {user['email']}"),
            html.H4("Blogs"),
            html.Ul([html.Li(blog) for blog in user['blogs']])
        ])
    return html.P("Failed to load user profile")
