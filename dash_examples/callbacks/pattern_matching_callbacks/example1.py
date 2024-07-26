from dash import Dash, dcc, html, Input, Output, ALL, Patch, callback

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Button("Add Filter", id="add-filter-btn", n_clicks=0),
        html.Div(id="dropdown-container-div", children=[]),
        html.Div(id="dropdown-container-output-div"),
    ]
)


@callback(
    Output("dropdown-container-div", "children"), Input("add-filter-btn", "n_clicks")
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    new_dropdown = dcc.Dropdown(
        ["NYC", "MTL", "LA", "TOKYO"],
        id={"type_kk": "city-filter-dropdown", "index": n_clicks}, # id here is a dictionary (ID dictionary, keys & values are arbitrary)
    )
    patched_children.append(new_dropdown)
    return patched_children


# The call back is fired whenever one of the dropdowns is changed
@callback(
    Output("dropdown-container-output-div", "children"),
    Input({"type_kk": "city-filter-dropdown", "index": ALL}, "value"), # index is anything
)
def display_output(values):
    return html.Div(
        [html.Div(f"Dropdown {i + 1} = {value}") for (i, value) in enumerate(values)]
    )


if __name__ == "__main__":
    app.run(debug=True)
