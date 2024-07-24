import dash
from dash import dcc, html, Input, Output, ctx
import dash_mantine_components as dmc
from urllib.parse import parse_qs, urlencode
from pages.home import home_layout
from pages.page1 import page1_layout
from pages.page2 import page2_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(
            id="url", refresh=True
        ),  # ensure refresh=True to update page content based on URL changes
        html.Div(id="page-content"),
    ]
)

from pages import setup_pages

# Importing setup_pages function which will load all pages and callbacks
setup_pages(app)


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"), Input("url", "search")],
)
def display_page(pathname, search):
    print(f"tesing: {pathname}, {search}")

    query_params = parse_qs(search.lstrip("?"))
    name = query_params.get("name", [""])[0]

    if pathname == "/page1":
        return page1_layout(name)
    elif pathname == "/page2":
        return page2_layout(name)
    return home_layout


if __name__ == "__main__":
    app.run_server(debug=True)
