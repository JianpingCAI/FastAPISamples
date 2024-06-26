import dash_mantine_components as dmc
from dash import Dash

app = Dash(__name__)

app.layout = dmc.MantineProvider(
    dmc.Alert(
        "Hi from Dash Mantine Components. You can create some great looking dashboards using me!",
        title="Welcome!",
        color="violet",
    )
)

if __name__ == "__main__":
    app.run_server()
