from dash import Dash, html, dcc, Input, Output, Patch, callback
import plotly.express as px

app = Dash(__name__)

# Get data
df = px.data.election()[:20]
# Create figure based on data
fig = px.bar(df, x="district")

app.layout = html.Div(
    [
        dcc.Dropdown(
            ["Coderre", "Joly", "Bergeron"], id="candidate-select", value="Joly"
        ),
        dcc.Graph(figure=fig, id="new-data-graph"),
    ]
)


@callback(Output("new-data-graph", "figure"), Input("candidate-select", "value"))
def update_figure(value):
    patched_fig = Patch()
    patched_fig["data"][0]["y"] = df[value].values
    return patched_fig


if __name__ == "__main__":
    app.run(debug=True)
