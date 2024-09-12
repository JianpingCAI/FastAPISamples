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
            rowData=initial_row_data,
            dashGridOptions={"rowSelection": "single", "editType": "fullRow"},
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
    State("grid", "rowData"),
    prevent_initial_call="initial_duplicate",
)
def add_row(n_clicks, row_data):
    if n_clicks > 0:
        # Create a new row with a unique ID
        new_row = {"id": str(uuid.uuid4()), "name": "", "species": ""}

        # Create the row transaction for adding a new row
        row_transaction = {"add": [new_row], "addIndex": len(row_data)}

        return row_transaction, new_row["id"]

    return {}, None


# Client-side callback to trigger cell editing
app.clientside_callback(
    """ (row_id, id) => {
        if (row_id) {
            // Access the grid API asynchronously
            dash_ag_grid.getApiAsync(id).then((grid) => {
                setTimeout(() => {
                    const rowIndex = grid.getDisplayedRowCount() - 1;  // Get the new row's index
                    grid.startEditingCell({rowIndex: rowIndex, colKey: 'name'});  // Start editing the new row
                }, 100);  // Delay to ensure the new row is added
            });
        }
        return null;                                      
    }""",
    Output("dummy-store", "data"),  # Dummy output to fulfill Dash callback contract
    Input("dcc-new-row-id", "data"),
    State("grid", "id"),
    prevent_initial_call="initial_duplicate",
)

if __name__ == "__main__":
    app.run_server(debug=True)
