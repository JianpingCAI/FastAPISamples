# Similar structure for both page1.py and page2.py
from dash import html, dcc
import dash_mantine_components as dmc


def page1_layout(name):
    return dmc.MantineProvider(
        children=[
            html.H1("Page 1"),
            html.Div(f"Hello, {name}! Welcome to Page 1."),
            html.Br(),
            dcc.Link("Go to Home", href="/"),
            html.Br(),
            dcc.Link("Go to Page 2", href=f"/page2?name={name}"),
        ]
    )
