from dash import Dash, html, dcc, Input, Output, Patch, callback
from plotly import graph_objects as go

app = Dash(__name__)

x = [
    "Product A",
    "Product C",
    "Product D",
    "Product E",
]
y = [20, 14, 23, 8]

fig = go.Figure(data=[go.Bar(x=x, y=y)])

app.layout = html.Div(
    [
        html.Button("Reverse Items", id="reverse-button"),
        dcc.Graph(figure=fig, id="reverse-example"),
    ]
)


@callback(Output("reverse-example", "figure"), Input("reverse-button", "n_clicks"))
def add_data_to_fig(n_clicks):
    patched_figure = Patch()
    patched_figure["data"][0]["x"].reverse()
    patched_figure["data"][0]["y"].reverse()
    return patched_figure


if __name__ == "__main__":
    app.run(debug=True)
