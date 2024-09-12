import dash
from dash import html, dcc, Input, Output, State, callback
import dash_ag_grid as dag
import uuid

app = dash.Dash(__name__)

# Initial Data for the grid
initial_row_data = [
    {"id": str(uuid.uuid4()), "name": "Plant A", "species": "Fern"},
    {"id": str(uuid.uuid4()), "name": "Plant B", "species": "Cactus"},
]

# Column Definitions
column_defs = [
    {"headerName": "ID", "field": "id", "editable": False},
    {"headerName": "Name", "field": "name", "editable": True},
    {"headerName": "Species", "field": "species", "editable": True},
]

# Layout
app.layout = html.Div(
    [
        dag.AgGrid(
            id="grid",
            columnDefs=column_defs,
            rowData=initial_row_data,  # Initialize with the original rows only once
            dashGridOptions={
                "rowSelection": "single",
                "editType": "fullRow",
            },
            getRowId="params.data.id",  # Set the unique ID property
        ),
        html.Button("Add Row", id="add-row-btn", n_clicks=0),
        dcc.Store(id="dcc-new-row-id"),
        dcc.Store(id="dummy-store"),  # Dummy output store to prevent errors
    ]
)


# Python callback to handle row addition
@callback(
    Output("grid", "rowTransaction", allow_duplicate=True),
    Output("dcc-new-row-id", "data", allow_duplicate=True),
    Input("add-row-btn", "n_clicks"),
    prevent_initial_call=True,
)
def add_row(n_clicks):
    if n_clicks > 0:
        # Create a new row with a unique ID
        new_row = {"id": str(uuid.uuid4()), "name": "", "species": ""}

        # Only add the new row, no need to manage existing data manually
        row_transaction = {"add": [new_row]}

        print(f"new_row: {new_row}")
        return row_transaction, new_row["id"]

    return {}, None


# Client-side callback to trigger cell editing
app.clientside_callback(
    "window.dagAPIFuncs.startEditingNewRow",
    Output("dummy-store", "data"),  # Dummy output to fulfill Dash callback contract
    Input("dcc-new-row-id", "data"),
    State("grid", "id"),
    prevent_initial_call=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
