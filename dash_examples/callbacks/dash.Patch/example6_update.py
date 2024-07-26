from dash import Dash, dcc, html, Input, Output, Patch, callback

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Button("Add options", id="add-options"),
        dcc.RadioItems(
            options={
                "New York City": "New York City",
                "Montreal": "Montreal",
                "San Francisco": "San Francisco",
            },
            value="Montreal",
            id="city-dd",
        ),
        html.Div(id="city-output-container"),
    ]
)


@callback(Output("city-output-container", "children"), Input("city-dd", "value"))
def update_output(value):
    return f"You have selected {value}"


@callback(
    Output("city-dd", "options"),
    Input("add-options", "n_clicks"),
    prevent_initial_call=True,
)
def update_output(n_clicks):
    patched_dropdown = Patch()
    european_cities = {"Paris": "Paris", "London": "London", "Berlin": "Berlin"}
    patched_dropdown.update(european_cities)
    return patched_dropdown


if __name__ == "__main__":
    app.run(debug=True)
