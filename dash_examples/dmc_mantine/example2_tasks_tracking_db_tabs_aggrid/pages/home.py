import dash
import dash_mantine_components as dmc

dash.register_page(__name__, path="/")

layout = dmc.MantineProvider(
    [
        dmc.Title("Task Tracker Home", order=1),
        dmc.Text("Welcome to the Task Tracker App!", size="md"),
    ]
)
