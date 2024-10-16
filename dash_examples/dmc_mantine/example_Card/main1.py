import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

external_stylesheets = [dbc.themes.COSMO, dbc.icons.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


card_template = lambda: dbc.Card(
    dbc.CardBody(
        [
            # Optional title in the card
            html.H5("Card Title", className="card-title"),
            # Checklist inside the card
            dcc.Checklist(
                options=[
                    {"label": "Option 1", "value": "1"},
                    {"label": "Option 2", "value": "2"},
                    {"label": "Option 3", "value": "3"},
                    {"label": "Option 4", "value": "4"},
                    {"label": "Option 5", "value": "5"},
                ],
                value=[],  # Initial selected values
            ),
        ]
    ),
    style={
        "width": "100%",  # Adjust the width based on the column size
        "height": 275,  # Fixed height
        "background-color": "#d5f5e3",  # Light green background
        "border": "1px solid #ccc",  # Border styling
        "border-radius": "10px",  # Rounded corners
        "box-shadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Light shadow
    },
    outline=True,  # Optionally have an outline border
)

card1 = card_template()
card2 = card_template()
card3 = card_template()

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([], xs=2, sm=2, md=2, lg=2),
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(card1, style={"flex": "1"}),
                            dbc.Col(card2, style={"flex": "1"}),
                            dbc.Col(card3, style={"flex": "1"}),
                        ],
                        style={
                            "display": "flex",
                            "flex-wrap": "nowrap",
                            "justify-content": "center",
                        },
                    ),
                    xs=10,
                    sm=10,
                    md=10,
                    lg=10,
                ),
            ],
            justify="center",
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
