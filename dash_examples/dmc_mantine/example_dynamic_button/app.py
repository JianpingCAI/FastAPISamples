import copy
import dash
from dash import html, Input, Output, State, clientside_callback, dcc
import dash_ag_grid as dag
import dash_mantine_components as dmc
import logging

# Set up logging to output debug messages
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = dash.Dash(__name__)

# Initial rowData should be defined and stored in a Store for easier management
initial_row_data = [
    {"task_name": "Task 1", "id": 1, "edit_mode": False},
    {"task_name": "Task 2", "id": 2, "edit_mode": False},
]

cellStyle2 = {
    "styleConditions": [
        {
            "condition": "params.data.edit_mode === false",
            "style": {"backgroundColor": "white"},
        },
        {
            "condition": "params.data.edit_mode === true",
            "style": {"backgroundColor": "lightBlue"},
        },
    ],
    "defaultStyle": {"backgroundColor": "white"},
}

cellStyle = {
    "function": "params.data.edit_mode? {'backgroundColor': 'lightBlue'} : {'backgroundColor': 'white'}"
}

app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="changed_cell"),
        dag.AgGrid(
            id="example-table",
            columnDefs=[
                {
                    "headerName": "Task Name",
                    "field": "task_name",
                    # conditionally enables editing
                    "editable": {"function": "params.data.edit_mode == true"},
                    "cellStyle": cellStyle,
                },
                {
                    "headerName": "Action",
                    "cellRenderer": "DMC_Action_Button",
                    "cellRendererParams": {"action": "edit"},
                },
            ],
            rowData=initial_row_data,
            dashGridOptions={"rowSelection": "single"},
            getRowId="params.data.id",
        ),
        html.Div(id="output"),
    ]
)


# @app.callback(
#     Output("example-table", "rowData", allow_duplicate=True),
#     Input("example-table", "cellRendererData"),
#     Input("example-table", "rowData"),
#     prevent_initial_call=True,
# )
# def handle_edit_save(data, rows_data):
#     if data is None or "value" not in data:
#         raise dash.exceptions.PreventUpdate

#     # logging.debug("old: %s", {data.get("value", {})})
#     logging.debug("input: %s", data)

#     # Get the row ID from the data received
#     row_id = data["value"]["id"]
#     prev_edit_mode = data["value"]["edit_mode"]
#     to_be_editable = not prev_edit_mode

#     logging.debug(f"to_be_editable: {to_be_editable}")

#     # Save the changes
#     if to_be_editable:
#         # Make cells edit_mode
#         for row in rows_data:
#             if row["id"] == row_id:
#                 row["edit_mode"] = True
#                 break
#     else:
#         # Save the changes
#         for row in rows_data:
#             if row["id"] == row_id:
#                 row["edit_mode"] = False
#                 break

#     logging.debug("new: %s", rows_data)

#     return rows_data


# Transaction Update - rowTransaction
@app.callback(
    Output("example-table", "rowTransaction"),
    Output("changed_cell", "data"),
    Input("example-table", "cellRendererData"),
    State("example-table", "rowData"),
)
def handle_edit_save(data, rows_data):
    if data is None or "value" not in data:
        raise dash.exceptions.PreventUpdate

    # logging.debug("old: %s", {data.get("value", {})})
    logging.debug("input: %s", data)
    logging.debug("rows_data: %s", rows_data)

    # Get the row ID from the data received
    row_id = data["value"]["id"]
    prev_edit_mode = data["value"]["edit_mode"]
    logging.debug(f"prev_edit_mode: {prev_edit_mode}")

    to_be_editable = not data["value"]["edit_mode"]
    logging.debug(f"to_be_editable: {to_be_editable}")

    # Save the changes
    if to_be_editable:
        # Make cells edit_mode
        for row in rows_data:
            if row["id"] == row_id:
                new_row = copy.deepcopy(row)
                new_row["edit_mode"] = True
                row["edit_mode"] = True

                # logging.debug("new_row: %s", new_row)
                # logging.debug("rows_data: %s", rows_data)
                return {"update": [copy.deepcopy(row)]}, row
    else:
        # Save the changes
        for row in rows_data:
            if row["id"] == row_id:
                new_row = copy.deepcopy(row)
                new_row["edit_mode"] = False
                row["edit_mode"] = False

                # logging.debug("new_row-4: %s", new_row)
                # logging.debug("rows_data: %s", rows_data)
                return {"update": [copy.deepcopy(row)]}, row

    # logging.debug("new: %s", rows_data)

    return dash.no_update, dash.no_update


clientside_callback(
    """async function (changed_row) {
        gridApi = await dash_ag_grid.getApiAsync('example-table')
        const rowNode = gridApi.getRowNode(changed_row.id);
        gridApi.refreshCells({force: true, rowNodes: [rowNode], columns: ['task_name']})
        console.log('row1', changed_row)
        return window.dash_clientside.no_update    
    }""",
    Output("output", "children"),
    Input("changed_cell", "data"),
    # prevent_intial_Call=True,
)

# clientside_callback(
#     """async function (changed_row) {
#         gridApi = await dash_ag_grid.getApiAsync('example-table')
#         const rowNode = gridApi.getRowNode(changed_row.id);
#         gridApi.refreshCells({force: true, columns: ['task_name']})
#         console.log('row1', changed_row)
#         return window.dash_clientside.no_update    
#     }""",
#     Output("output", "children"),
#     Input("changed_cell", "data"),
#     # prevent_intial_Call=True,
# )


if __name__ == "__main__":
    app.run_server(debug=True)
