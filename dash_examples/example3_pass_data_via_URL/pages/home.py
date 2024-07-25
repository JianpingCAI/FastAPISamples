from dash import html, dcc, Input, Output, State
import dash
import dash_mantine_components as dmc
from urllib.parse import urlencode

home_layout = dmc.MantineProvider(
    children=[
        html.H1("Home Page"),
        dcc.Input(id="input-name", type="text", placeholder="Enter your name"),
        html.Button("Submit", id="submit-name"),
        # html.Br(),
        # dcc.Link("Go to Page 1", href="/page1", id="link-page1"),
        # html.Br(),
        # dcc.Link("Go to Page 2", href="/page2", id="link-page2"),
        dcc.Location(id="redirect", refresh=True),
    ]
)


# Function to register callbacks
def register_callbacks(app):
    @app.callback(
        Output("redirect", "href"),
        Input("submit-name", "n_clicks"),
        State("input-name", "value"),
    )
    def set_query(n_clicks, value):
        if n_clicks:
            return f"/page1?name={value}"  # Redirect to Page 1 with the name in the query
        return dash.no_update
