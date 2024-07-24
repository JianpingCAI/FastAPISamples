from dash import html, dcc
import dash_mantine_components as dmc

home_layout = dmc.MantineProvider(
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
