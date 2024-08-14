import dash
from dash import html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    # suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.SPACELAB],
)
server = app.server

app.layout = dmc.MantineProvider(
    [
        dmc.Paper(
            p="md",
            children=[
                html.Nav(
                    [
                        dmc.Anchor("Home", href="/", style={"marginRight": "10px"}),
                        dmc.Anchor(
                            "Tasks", href="/tasks", style={"marginRight": "10px"}
                        ),
                    ],
                    style={"padding": "10px"},
                )
            ],
            style={"backgroundColor": "#2c3e50", "color": "#ecf0f1"},
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
