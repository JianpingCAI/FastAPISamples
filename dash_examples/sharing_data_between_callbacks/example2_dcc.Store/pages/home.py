from dash import html, register_page, no_update, callback
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc

register_page(__name__, path="/")

layout = dmc.MantineProvider(
    children=[
        html.H1("Home Page"),
        dmc.TextInput(
            label="Enter Name",
            id="input-name",
            placeholder="Your name",
            size="md",
            radius="sm",
        ),
        dmc.TextInput(
            label="Enter Age",
            id="input-age",
            placeholder="Your age",
            size="md",
            radius="sm",
        ),
        dmc.TextInput(
            label="Enter Email",
            id="input-email",
            placeholder="Your email",
            size="md",
            radius="sm",
        ),
        dmc.Button(
            "Store Data",
            id="store-data-button",
            variant="outline",
            color="blue",
            radius="md",
            size="lg",
            mt=10,
        ),
        html.Div(id="home-output", style={"marginTop": "20px"}),
        html.Br(),
        dmc.Anchor("Go to Page 1", href="/page1", mt=20),
        html.Br(),
        dmc.Anchor("Go to Page 2", href="/page2", mt=10),
    ]
)


# Function to register callbacks
@callback(
    Output("shared-data", "data"),
    Output("home-output", "children"),
    Input("store-data-button", "n_clicks"),
    State("input-name", "value"),
    State("input-age", "value"),
    State("input-email", "value"),
)
def store_data(n_clicks, name, age, email):
    if n_clicks:
        # Note: the data needs to be serilized into a JSON string before being placed in storage
        data = {"name": name, "age": age, "email": email}
        print("Data stored:", data)  # Debug print
        return data, f"Data stored: {data}"
    return no_update, "Click the button to store data."
