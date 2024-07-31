from dash import html, register_page, callback
import dash_mantine_components as dmc
from dash.dependencies import Input, Output

register_page(__name__, path='/page1')

layout = dmc.MantineProvider(
    children=[
        html.H1("Page 1"),
        dmc.Anchor("Go to Home Page", href="/", mt=10),
        html.Br(),
        dmc.Anchor("Go to Page 2", href="/page2", mt=10),
        html.Br(),
        html.Div(id="page1-output", style={"marginTop": "20px"}),
    ]
)

# Function to register callbacks
@callback(Output("page1-output", "children"), Input("shared-data", "data"))
def display_data_page1(data):
    if data:
        return html.Div(
            [
                html.P(f"Name: {data['name']}"),
                html.P(f"Age: {data['age']}"),
                html.P(f"Email: {data['email']}"),
            ]
        )
    return "No data stored yet."
