from dash import Dash, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = Dash(__name__)

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light", "primaryColor": "blue"},
    children=[
        dmc.Container(
            [
                dmc.Title("Icons in Dash", ta="center"),
                dmc.Group(
                    [
                        DashIconify(icon="mdi:home", width=40),
                        DashIconify(icon="mdi:account", width=40),
                        DashIconify(icon="mdi:star", width=40),
                    ],
                ),
                dmc.Text(
                    "Above are some icons using Dash Iconify.", ta="center", mt="md"
                ),
            ]
        )
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
