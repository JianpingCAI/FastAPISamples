from dash import Dash, dash_table, html, Input, Output, Patch, callback
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Button("Delete first row", id="delete-button-1"),
        dash_table.DataTable(
            df.to_dict("records"),
            [{"name": i, "id": i} for i in df.columns],
            id="table-example-for-delete-1",
        ),
    ]
)


# Deleting row at index 0 in the data when the delete button is clicked
@callback(
    Output("table-example-for-delete-1", "data"), Input("delete-button-1", "n_clicks")
)
def delete_records(n_clicks):
    patched_table = Patch()
    del patched_table[0]
    return patched_table


if __name__ == "__main__":
    app.run(debug=True)
