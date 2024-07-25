# data.py
import pandas as pd


def load_data() -> pd.DataFrame:
    return pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
    )
