# callbacks.py
from dash import Dash, Output, Input
import plotly.express as px
from homepage_layout import HomePage
from homepage_constants import ComponentProps

# Note: Auto component IDs won't work with dynamic callback content unless the component variables are defined out of the callback scope.
#       Additionally, they are not compatible with Pattern-Matching Callbacks.

# Principle: Dash Callbacks must never modify variables outside of their scope.


class Homepage_Callbacks:
    def __init__(self, app: Dash, layout: HomePage) -> None:
        self.app = app
        self.page: HomePage = layout
        self.register_callbacks()

    def register_callbacks(self) -> None:

        @self.app.callback(
            Output(self.page.graph, ComponentProps.FIGURE.value),
            Input(self.page.radio_items, ComponentProps.VALUE.value),
        )
        def update_graph(selected_column: str) -> px.histogram:

            fig = px.histogram(
                self.page.df, x="continent", y=selected_column, histfunc="avg"
            )
            return fig
