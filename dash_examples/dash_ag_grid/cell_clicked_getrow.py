import dash
from dash import html, dcc, Input, Output
import dash_ag_grid as dag
import pandas as pd

app = dash.Dash(__name__)

# Sample data
df = pd.DataFrame(
    {
        "make": ["Toyota", "Ford", "BMW"],
        "model": ["Corolla", "Mustang", "X5"],
        "price": [35000, 45000, 55000],
    }
)

columnDefs = [
    {"headerName": "Make", "field": "make"},
    {"headerName": "Model", "field": "model"},
    {"headerName": "Price", "field": "price"},
]

# Create AG Grid
grid = dag.AgGrid(
    id="my-grid",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef={"sortable": True, "filter": True, "editable": True},
    # Enable cell click events
    # cellEvents=["cellClicked"],
)

app.layout = html.Div([grid, html.Div(id="output")])


@app.callback(Output("output", "children"), Input("my-grid", "cellClicked"))
def display_row_data(cell_clicked):
    print(f"cell_clicked: {cell_clicked}")
    if cell_clicked:
        # Extract row data from the event
        row_data = cell_clicked.get("data", {})
        return html.Pre(str(row_data))
    return "Click a cell to see row data"


if __name__ == "__main__":
    app.run_server(debug=True)
