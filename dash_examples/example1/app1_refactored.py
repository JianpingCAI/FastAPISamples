# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px


# Incorporate data
def load_data():
    return pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
    )


# Initialize the app
def create_app():
    app = Dash(__name__)
    return app


# Define the layout
def create_layout(app, df):
    app.layout = html.Div(
        [
            html.Div("My First App with Data, Graph, and Controls"),
            html.Hr(),
            dcc.RadioItems(
                options=[
                    {"label": col, "value": col}
                    for col in ["pop", "lifeExp", "gdpPercap"]
                ],
                value="lifeExp",
                id="radio-item-example",
            ),
            dash_table.DataTable(data=df.to_dict("records"), page_size=6),
            dcc.Graph(figure={}, id="graph-example"),
        ]
    )


# Define callbacks
def register_callbacks(app, df):
    @app.callback(
        Output("graph-example", "figure"), Input("radio-item-example", "value")
    )
    def update_graph(selected_column):
        fig = px.histogram(df, x="continent", y=selected_column, histfunc="avg")
        return fig


# Main function to run the app
def main():
    df = load_data()
    app = create_app()
    create_layout(app, df)
    register_callbacks(app, df)

    app.run_server(debug=True)


# Run the app
if __name__ == "__main__":
    main()
