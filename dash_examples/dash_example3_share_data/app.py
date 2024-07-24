import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_mantine_components as dmc

# Pre-import layouts to ensure they are initialized properly
from pages.home import home_layout
from pages.page1 import page1_layout
from pages.page2 import page2_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="shared-data", storage_type="session"),
        html.Div(id="page-content"),
    ]
)


# Simplified callback for page navigation
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/page1":
        return page1_layout
    elif pathname == "/page2":
        return page2_layout
    else:
        return home_layout


# Import callbacks to register them
from callbacks import *
# import callbacks --> this won't work!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Correct Callback Registration: By changing import callbacks to from callbacks import *, 
# we ensured that all callback decorators were executed, registering the callbacks correctly with the Dash app instance. 
# However, for better practices, explicit imports or an initialization function were recommended.

if __name__ == "__main__":
    app.run_server(debug=True)

