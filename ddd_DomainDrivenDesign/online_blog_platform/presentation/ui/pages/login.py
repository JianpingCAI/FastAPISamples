from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import requests

layout = html.Div(
    [
        html.H2("Login"),
        dcc.Input(id="username", type="text", placeholder="Username"),
        dcc.Input(id="password", type="password", placeholder="Password"),
        html.Button("Login", id="login-button", n_clicks=0),
        html.Div(id="login-output"),
    ]
)


# Callback to handle the login
@callback(
    Output("login-output", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
)
def login_user(n_clicks, username, password):
    if n_clicks > 0:
        response = requests.post(
            "http://localhost:8000/token",
            data={"username": username, "password": password},
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            # Save the token in the session storage for later use
            return html.P("Login successful!")
        else:
            return html.P("Login failed. Please check your credentials.")
    return ""
