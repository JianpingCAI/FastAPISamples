from dash import Dash, Input, Output, State, html, dcc, MATCH
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

# Initialize the app with Bootstrap stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data for the grid
row_data = [
    {"id": 1, "make": "Toyota", "model": "Celica", "price": 35000},
    {"id": 2, "make": "Ford", "model": "Mondeo", "price": 32000},
    {"id": 3, "make": "Porsche", "model": "Boxster", "price": 72000},
]

# Column definitions
column_defs = [
    {"headerName": "Make", "field": "make"},
    {"headerName": "Model", "field": "model"},
    {"headerName": "Price", "field": "price"},
]

# Layout with AG Grid and a hidden modal placeholder
app.layout = html.Div(
    [
        dag.AgGrid(
            id="my-grid",
            columnDefs=column_defs,
            rowData=row_data,
            columnSize="sizeToFit",
            getRowId="params.data.id",  # Enable row identification by unique ID
            dashGridOptions={"rowSelection": "single"},
        ),
        html.Div(id="modal-container"),  # Placeholder for dynamically generated modal
    ]
)


# Callback to dynamically create and display modal based on row selection
@app.callback(
    Output("modal-container", "children"),
    Input("my-grid", "selectedRows"),  # Trigger callback on selectedRows change
    prevent_initial_call=True,
)
def display_modal(selected_rows):
    if selected_rows:
        # Access the first selected row data (since rowSelection is 'single')
        selected_row = selected_rows[0]

        # Create a modal dynamically based on the selected row data
        modal = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(f"Details for {selected_row['make']}")),
                dbc.ModalBody(
                    [
                        html.P(f"Model: {selected_row['model']}"),
                        html.P(f"Price: ${selected_row['price']:,}"),
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id={"type": "close-modal-button", "index": 0},
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id={"type": "dynamic-modal", "index": 0},
            is_open=True,  # Open the modal
        )
        return modal  # Return the dynamically created modal
    return None  # No modal if no row is selected


# Callback to close the modal
@app.callback(
    Output({"type": "dynamic-modal", "index": 0}, "is_open"),
    Input({"type": "close-modal-button", "index": 0}, "n_clicks"),
    prevent_initial_call=True,  # Prevents callback from running on initial page load
)
def close_modal(n_clicks):
    # Check if the modal exists to avoid triggering errors
    if n_clicks:
        return False  # Close the modal
    return True


if __name__ == "__main__":
    app.run_server(debug=True)
