import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import session
import uuid

# Initialize the Dash app and enable server-side sessions
app = dash.Dash(__name__)
app.server.secret_key = "supersecretkey"

# Define the layout
app.layout = html.Div(
    [
        html.H1("User-Specific Counter Example"),
        html.Button("Increment Counter", id="increment-button"),
        html.Div(id="counter-display"),
    ]
)


# Callback to initialize session-specific counter
@app.callback(
    Output("counter-display", "children"),
    Input("increment-button", "n_clicks"),
    prevent_initial_call=True,
)
def update_counter(n_clicks):
    if "counter" not in session:
        session["counter"] = 0

    # Increment the session-specific counter
    session["counter"] += 1
    return f"User-Specific Counter Value: {session['counter']}"


if __name__ == "__main__":
    app.run_server(debug=True)
