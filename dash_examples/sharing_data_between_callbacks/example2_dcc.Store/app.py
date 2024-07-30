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


if __name__ == "__main__":
    app.run_server(debug=True)
