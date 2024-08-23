from dash import Dash, html
from dash.dependencies import Output, Input

app = Dash(__name__)

app.layout = html.Div(
    [html.Button("Click me", id="home-button"), html.Div(id="home-output")]
)

app.clientside_callback(
    "dash_clientside.clientside.home_function",
    Output("home-output", "children"),
    Input("home-button", "n_clicks"),
)

if __name__ == "__main__":
    app.run_server(debug=True)
