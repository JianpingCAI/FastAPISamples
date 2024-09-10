from typing import Dict, List
import dash
from dash import html, Input, Output, State, callback_context
import dash_ag_grid as dag
import dash_mantine_components as dmc

# Sample data for AG Grid
row_data = [
    {"id": 0, "name": "Bob", "age": 30, "email": "bob@example.com"},
    {"id": 1, "name": "Charlie", "age": 35, "email": "charlie@example.com"},
    {"id": 2, "name": "Alice", "age": 25, "email": "alice@example.com"},
]

column_defs = [
    {"headerName": "Name", "field": "name"},
    {"headerName": "Age", "field": "age"},
    {"headerName": "Email", "field": "email"},
]

app = dash.Dash(__name__)

# Layout includes AG Grid and a container for the modal
app.layout = dmc.MantineProvider(
    [
        dag.AgGrid(
            id="my-grid",
            rowData=row_data,
            columnDefs=column_defs,
            columnSize="sizeToFit",
            className="ag-theme-alpine",
            dashGridOptions={"rowSelection": "single"},
            getRowId="params.data.id",
            style={"height": "200px", "width": "600px"},
        ),
        # This container will dynamically hold the modal
        html.Div(id="modal-container"),
    ]
)


# Callback to dynamically create and show the modal when a cell is clicked
@app.callback(
    Output("modal-container", "children", allow_duplicate=True),
    Input("my-grid", "selectedRows"),
    prevent_initial_call="initial_duplicate",
)
def create_modal_on_row_selection(selected_rows: List[Dict]):
    print(f"selected_rows: {selected_rows}")
    if selected_rows and len(selected_rows) > 0:

        # trigered_id = callback_context.triggered_id
        # print(f"triggered_id: {trigered_id}")
        # Extract row data from the clicked cell
        # print(selected_rows)
        row_data = selected_rows[0]
        # row_index = selected_rows["rowIndex"]  # Store the row index

        # Dynamically create the modal with input fields for editing
        modal = dmc.Modal(
            # id=f"modal-{row_index}",  # Dynamically assign ID based on row index
            id={"type": "dynamic-modal", "index": 0},
            title="Edit Row Details",
            opened=True,  # Modal opens dynamically
            children=[
                dmc.TextInput(
                    id={"type": "edit-name", "index": 0},
                    label="Name",
                    value=row_data["name"],
                ),
                dmc.TextInput(
                    id={"type": "edit-age", "index": 0},
                    label="Age",
                    value=str(row_data["age"]),
                ),
                dmc.TextInput(
                    id={"type": "edit-email", "index": 0},
                    label="Email",
                    value=row_data["email"],
                ),
                dmc.Button("Save", id={"type": "save-btn", "index": 0}),
                dmc.Button(
                    "Cancel", id={"type": "cancel-btn", "index": 0}
                ),  # Cancel button to close the modal
            ],
        )
        return [modal]  # Return the modal to be displayed dynamically

    # if no rows are selected, remove the modal
    return []


# Callback to close the modal when the Cancel button is clicked
@app.callback(
    Output("modal-container", "children", allow_duplicate=True),
    Output("my-grid", "selectedRows", allow_duplicate=True),
    Input({"type": "cancel-btn", "index": 0}, "n_clicks"),
    prevent_initial_call="initial_duplicate",
)
def close_modal_on_cancel(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    print(f"cancel-button n_clicks: {n_clicks}")
    # Check if the "Cancel" button was clicked
    if n_clicks > 0:
        print("umount modal")
        return [], []

    raise dash.exceptions.PreventUpdate


# Callback to update the grid after saving the edited row details
@app.callback(
    Output("my-grid", "rowTransaction"),  # Static output for the grid data update
    Output("modal-container", "children", allow_duplicate=True),
    Output("my-grid", "selectedRows", allow_duplicate=True),
    Input({"type": "save-btn", "index": 0}, "n_clicks"),
    State({"type": "edit-name", "index": 0}, "value"),
    State({"type": "edit-age", "index": 0}, "value"),
    State({"type": "edit-email", "index": 0}, "value"),
    State("my-grid", "rowData"),
    State("my-grid", "cellClicked"),
    prevent_initial_call="initial_duplicate",
)
def save_edits(save_btn_clicks, name, age, email, current_rows_data, cell_clicked):
    # Check if the "Save" button was clicked and a cell is selected
    if save_btn_clicks and save_btn_clicks > 0 and cell_clicked:
        # Get the index of the clicked row from the cellClicked event
        row_index = cell_clicked["rowIndex"]

        # Update the row data with the new input values
        row_updated = {
            "id": current_rows_data[row_index]["id"],
            "name": name,
            "age": int(age),  # Convert age to integer
            "email": email,
        }

        print(f"update row {row_index}: {row_updated}")
        # Return the updated rowData for the grid
        return {"update": [row_updated]}, [], []

    return (
        dash.no_update,
        dash.no_update,
        [],
    )  # Return the existing data if no changes were made


if __name__ == "__main__":
    app.run_server(debug=True)
