# callbacks.py
from dash import callback, Output, Input
import plotly.express as px
from constants import ComponentIDs, ComponentProps

class Callbacks:
    def __init__(self, app, df):
        self.app = app
        self.df = df
        self.register_callbacks()

    def register_callbacks(self):
        @self.app.callback(
            Output(ComponentIDs.GRAPH.value, ComponentProps.FIGURE.value),
            Input(ComponentIDs.RADIO_ITEM.value, ComponentProps.VALUE.value)
        )
        def update_graph(selected_column):
            fig = px.histogram(self.df, x="continent", y=selected_column, histfunc="avg")
            return fig
