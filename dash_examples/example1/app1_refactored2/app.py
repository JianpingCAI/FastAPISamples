# app.py
from dash import Dash
from data import load_data
from layout import create_layout
from callbacks import Callbacks


def main():
    df = load_data()
    app = Dash(__name__)
    app.layout = create_layout(df)
    Callbacks(app, df)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
