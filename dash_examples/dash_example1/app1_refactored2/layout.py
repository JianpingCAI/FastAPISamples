# layout.py
from dash import html, dash_table, dcc
from constants import ComponentIDs

def create_radio_items():
    return dcc.RadioItems(
        options=[{"label": col, "value": col} for col in ["pop", "lifeExp", "gdpPercap"]],
        value="lifeExp",
        id=ComponentIDs.RADIO_ITEM.value
    )

def create_data_table(df):
    return dash_table.DataTable(
        data=df.to_dict("records"),
        page_size=6
    )

def create_graph():
    return dcc.Graph(
        figure={},
        id=ComponentIDs.GRAPH.value
    )

def create_layout(df):
    return html.Div([
        html.Div("My First App with Data, Graph, and Controls"),
        html.Hr(),
        create_radio_items(),
        create_data_table(df),
        create_graph()
    ])
