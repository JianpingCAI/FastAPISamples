import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import threading
import time

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    [
        dcc.Store(id="task-status-store", data={"status": "not started"}),
        html.Button("Start Long Task", id="start-task", n_clicks=0),
        html.Div(id="task-status"),
        dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
    ]
)


# Background task function
def long_task(update_store_data):
    time.sleep(2)  # Simulate a long task
    update_store_data("completed")


# Callback to start the long task asynchronously
@app.callback(
    Output("task-status", "children", allow_duplicate=True),
    Output("task-status-store", "data"),
    Input("start-task", "n_clicks"),
    State("task-status-store", "data"),
    prevent_initial_call=True,
)
def start_long_task(n_clicks, store_data):
    if n_clicks > 0:
        store_data["status"] = "in progress"
        # Start a background thread to run the long task
        threading.Thread(target=long_task).start()
        return "Task Started...", store_data


# Callback to update the status periodically
@app.callback(
    Output("task-status", "children", allow_duplicate=True),
    Input("interval-component", "n_intervals"),
    State("task-status-store", "data"),
    prevent_initial_call=True,
)
def update_task_status(n, store_data):
    if store_data["status"] == "completed":
        return "Task Completed"
    elif store_data["status"] == "in progress":
        return "Task in Progress..."
    return "Click the button to start the task."


if __name__ == "__main__":
    app.run_server(debug=True)
