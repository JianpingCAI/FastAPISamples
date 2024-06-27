# app.py
from dash import Dash
from homepage_data import load_data
from homepage_layout import HomePage
from homepage_callbacks import (
    Homepage_Callbacks,
)
import pandas as pd


def main() -> None:
    df: pd.DataFrame = load_data()
    app: Dash = Dash(__name__)

    # Initialize layout with data
    homepage: HomePage = HomePage(df)
    app.layout = homepage.create_layout()

    # Register callbacks with component references
    Homepage_Callbacks(app, homepage)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
