from dash import Output, Input, State
from app import app
from dash import html
import dash

@app.callback(
    Output("shared-data", "data"),
    Output("home-output", "children"),
    Input("store-data-button", "n_clicks"),
    State("input-name", "value"),
    State("input-age", "value"),
    State("input-email", "value"),
)
def store_data(n_clicks, name, age, email):
    if n_clicks:
        data = {"name": name, "age": age, "email": email}
        print("Data stored:", data)  # Debug print
        return data, f"Data stored: {data}"
    return dash.no_update, "Click the button to store data."


@app.callback(Output("page1-output", "children"), Input("shared-data", "data"))
def display_data_page1(data):
    if data:
        return html.Div(
            [
                html.P(f"Name: {data['name']}"),
                html.P(f"Age: {data['age']}"),
                html.P(f"Email: {data['email']}"),
            ]
        )
    return "No data stored yet."


@app.callback(Output("page2-output", "children"), Input("shared-data", "data"))
def display_data_page2(data):
    if data:
        return html.Div(
            [
                html.P(f"Name: {data['name']}"),
                html.P(f"Age: {data['age']}"),
                html.P(f"Email: {data['email']}"),
            ]
        )
    return "No data stored yet."
