from dash import Dash, html, dcc, Input, Output, Patch, callback
import plotly.graph_objects as go

import datetime
import random

app = Dash(__name__)

fig = go.Figure()

app.layout = html.Div(
    [
        html.Button("Append", id="append-new-val"),
        dcc.Graph(figure=fig, id="append-example-graph"),
    ]
)


@callback(
    Output("append-example-graph", "figure"),
    Input("append-new-val", "n_clicks"),
    prevent_initial_call=True,
)
def add_data_to_fig(n_clicks):
    current_time = datetime.datetime.now()
    random_value = random.randrange(1, 30, 1)
    patched_figure = Patch()
    patched_figure["data"][0]["x"].append(current_time)
    patched_figure["data"][0]["y"].append(random_value)
    return patched_figure


if __name__ == "__main__":
    app.run(debug=True)
