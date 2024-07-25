# layout.py
from dash import html, dash_table, dcc
import pandas as pd
from dash.development.base_component import Component


class HomePage:

    def __init__(self, df: pd.DataFrame) -> None:

        self.df: pd.DataFrame = df
        self.radio_items: dcc.RadioItems = self.create_radio_items()
        self.data_table: dash_table.DataTable = self.create_data_table()
        self.graph: dcc.Graph = self.create_graph()

    def create_radio_items(self) -> dcc.RadioItems:
        return dcc.RadioItems(
            options=[
                {"label": col, "value": col} for col in ["pop", "lifeExp", "gdpPercap"]
            ],
            value="lifeExp",
            id="radio-item-example",
        )

    def create_data_table(self) -> dash_table.DataTable:
        return dash_table.DataTable(data=self.df.to_dict("records"), page_size=6)

    def create_graph(self) -> dcc.Graph:
        return dcc.Graph(figure={}, id="graph-example")

    def create_layout(self) -> Component:
        return html.Div(
            [
                html.Div("My First App with Data, Graph, and Controls"),
                html.Hr(),
                self.radio_items,
                self.data_table,
                self.graph,
            ]
        )
