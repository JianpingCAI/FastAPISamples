from dash import html
import dash_mantine_components as dmc

page2_layout = dmc.MantineProvider(
    children=[
        html.H1("Page 2"),
        dmc.Anchor("Go to Home Page", href="/", mt=10),
        html.Br(),
        dmc.Anchor("Go to Page 1", href="/page1", mt=10),
        html.Br(),
        html.Div(id="page2-output", style={"marginTop": "20px"}),
    ]
)
