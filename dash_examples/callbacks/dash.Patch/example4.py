from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    [
        html.Button("Add Filter", id="add-filter-2", n_clicks=0),
        html.Div(id="dropdown-container-2", children=[]),
        html.Div(id="dropdown-container-output-2"),
    ]
)


@callback(
    Output("dropdown-container-2", "children"),
    Input("add-filter-2", "n_clicks"),
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    new_dropdown = dcc.Dropdown(
        ["NYC", "MTL", "LA", "TOKYO"],
        id={"type": "filter-dropdown-2", "index": n_clicks},
    )
    patched_children.append(new_dropdown)
    return patched_children


@callback(
    Output("dropdown-container-output-2", "children"),
    Input({"type": "filter-dropdown-2", "index": ALL}, "value"),
)
def display_output(values):
    return html.Div(
        [
            html.Div("Dropdown {} = {}".format(i + 1, value))
            for (i, value) in enumerate(values)
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)
