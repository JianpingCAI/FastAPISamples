import json
import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import dash_mantine_components as dmc
import dash_iconify


data = {
    "ticker": ["AAPL", "MSFT", "AMZN", "GOOGL"],
    "price": [154.99, 268.65, 100.47, 96.75],
    "buy": ["Buy" for _ in range(4)],
    "sell": ["Sell" for _ in range(4)],
    "watch": ["Watch" for _ in range(4)],
}
df = pd.DataFrame(data)

columnDefs = [
    {
        "headerName": "Stock Ticker",
        "field": "ticker",
    },
    {
        "headerName": "Last Close Price",
        "type": "rightAligned",
        "field": "price",
        "valueFormatter": {"function": """d3.format("($,.2f")(params.value)"""},
    },
    {
        "field": "buy",
        "cellRenderer": "DMC_Button",
        "cellRendererParams": {
            "variant": "outline",
            "leftIcon": "ic:baseline-shopping-cart",
            "color": "green",
            "radius": "xl",
        },
    },
    {
        "field": "sell",
        "cellRenderer": "DMC_Button",
        "cellRendererParams": {
            "variant": "outline",
            "leftIcon": "ic:baseline-shopping-cart",
            "color": "red",
            "radius": "xl",
        },
    },
    {
        "field": "watch",
        "cellRenderer": "DMC_Button",
        "cellRendererParams": {
            "rightIcon": "ph:eye",
        },
    },
]


grid = dag.AgGrid(
    id="custom-component-dmc-btn-grid",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="autoSize",
    defaultColDef={"minWidth": 125},
)


app = Dash(__name__)

app.layout = dmc.MantineProvider(
    [
        html.Div(
            [
                dcc.Markdown(
                    "Example of cellRenderer with `dash-mantine-components` button  and `DashIconify` icons"
                ),
                grid,
                html.Div(id="custom-component-dmc-btn-value-changed"),
            ]
        )
    ]
)


@callback(
    Output("custom-component-dmc-btn-value-changed", "children"),
    Input("custom-component-dmc-btn-grid", "cellRendererData"),
)
def showChange(n):
    return json.dumps(n)


if __name__ == "__main__":
    app.run(debug=True)
