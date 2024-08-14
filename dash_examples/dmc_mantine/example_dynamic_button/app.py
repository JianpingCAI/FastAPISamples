import dash
from dash import html, Input, Output, State
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

cellStyle = {
    "styleConditions": [
        {
            "condition": "params.data.edit_mode == true",
            "style": {"backgroundColor": "red"},
        },
    ]
}

app.layout = dmc.MantineProvider(
    [
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
#     Output("example-table", "rowData"),
#     Input("example-table", "cellRendererData"),
#     Input("example-table", "rowData"),
# )
# def handle_edit_save(data, rows_data):
#     if data is None or "value" not in data:
#         raise dash.exceptions.PreventUpdate

#     # logging.debug("old: %s", {data.get("value", {})})
#     logging.debug("input: %s", data)

#     # Get the row ID from the data received
#     row_id = data["value"]["id"]
#     edit_mode = data["value"]["edit_mode"]

#     logging.debug(f"edit_mode: {edit_mode}")

#     # Save the changes
#     if edit_mode:
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
    new_edit_mode = not prev_edit_mode

    logging.debug(f"edit_mode: {prev_edit_mode}")

    # Save the changes
    if new_edit_mode:
        # Make cells edit_mode
        for row in rows_data:
            if row["id"] == row_id:
                logging.debug("row-1: %s", row)
                row["edit_mode"] = True
                logging.debug("row-2: %s", row)
                logging.debug("rows_data: %s", rows_data)
                return {"update": [row]}
    else:
        # Save the changes
        for row in rows_data:
            if row["id"] == row_id:
                logging.debug("row-3: %s", row)
                row["edit_mode"] = False
                logging.debug("row-4: %s", row)
                logging.debug("rows_data: %s", rows_data)
                return {"update": rows_data}

    # logging.debug("new: %s", rows_data)

    return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
