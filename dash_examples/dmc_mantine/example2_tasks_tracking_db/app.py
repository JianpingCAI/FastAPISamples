import dash
import dash_mantine_components as dmc
from dash import html

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

app.layout = dmc.MantineProvider(
    [
        dmc.Paper(
            p="md",
            children=[
                html.Nav(
                    [
                        dmc.Anchor("Home", href="/", style={"margin-right": "10px"}),
                        dmc.Anchor(
                            "Tasks", href="/tasks", style={"margin-right": "10px"}
                        ),
                        dmc.Anchor(
                            "Add Task", href="/add_task", style={"margin-right": "10px"}
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
