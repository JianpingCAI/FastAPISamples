import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Global variable to store the counter
counter = 0

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    [
        html.H1("Global Counter Example"),
        html.Button("Increment Counter", id="increment-button"),
        html.Div(id="counter-display"),
    ]
)


# Callback to update the counter
@app.callback(
    Output("counter-display", "children"),
    Input("increment-button", "n_clicks"),
    prevent_initial_call=True,
)
def update_counter(n_clicks):
    global counter
    # Increment the global counter
    counter += 1
    return f"Global Counter Value: {counter}"


if __name__ == "__main__":
    app.run_server(debug=True)
