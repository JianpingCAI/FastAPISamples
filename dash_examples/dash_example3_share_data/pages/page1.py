from dash import html
import dash_mantine_components as dmc

page1_layout = dmc.MantineProvider(
    children=[
        html.H1("Page 1"),
        dmc.Anchor("Go to Home Page", href="/", mt=10),
        html.Br(),
        dmc.Anchor("Go to Page 2", href="/page2", mt=10),
        html.Br(),
        html.Div(id="page1-output", style={"marginTop": "20px"}),
    ]
)
