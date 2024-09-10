from dash import Dash, Input, Output, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

from components.details_modal import DetailsModalComponent

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
        return DetailsModalComponent(
            modal_id={"type": "dynamic-modal", "index": 0}, selected_row=selected_row
        ).get_component()

    return None  # No modal if no row is selected


if __name__ == "__main__":
    app.run_server(debug=True)
