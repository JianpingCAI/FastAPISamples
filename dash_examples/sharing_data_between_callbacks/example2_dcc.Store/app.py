import dash
from dash import dcc
import dash_mantine_components as dmc

# - use_pages
# - dash.page_container

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
# app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="shared-data", storage_type="session"),
        # html.Div(id="page-content"),
        dash.page_container,
    ]
)

from pages import setup_pages

# Importing setup_pages function which will load all pages and callbacks
setup_pages(app)


# # Callback for page navigation
# @app.callback(Output("page-content", "children"), Input("url", "pathname"))
# def display_page(pathname):
#     if pathname == "/page1":
#         from pages.page1 import page1_layout

#         return page1_layout
#     elif pathname == "/page2":
#         from pages.page2 import page2_layout

#         return page2_layout
#     else:
#         from pages.home import home_layout

#         return home_layout


if __name__ == "__main__":
    app.run_server(debug=True)
