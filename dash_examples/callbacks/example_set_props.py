import dash_ag_grid as dag
from dash import Dash, Input, html, ctx, callback, set_props
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

rowData = [
    {"make": "Toyota", "model": "Celica", "price": 35000},
    {"make": "Ford", "model": "Mondeo", "price": 32000},
    {"make": "Porsche", "model": "Boxster", "price": 72000},
]

app.layout = html.Div(
    [
        dag.AgGrid(
            id="setprops-row-selection-popup",
            rowData=rowData,
            columnDefs=[{"field": i} for i in ["make", "model", "price"]],
            columnSize="sizeToFit",
            dashGridOptions={"rowSelection": "single", "animateRows": False},
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("More information about selected row"),
                dbc.ModalBody(id="setprops-row-selection-modal-content"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="setprops-row-selection-modal-close",
                        className="ml-auto",
                    )
                ),
            ],
            id="setprops-row-selection-modal",
        ),
    ]
)


@callback(
    Input("setprops-row-selection-popup", "selectedRows"),
    Input("setprops-row-selection-modal-close", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal(selection, _):
    if ctx.triggered_id == "setprops-row-selection-modal-close":
        # Close the modal
        set_props("setprops-row-selection-modal", {"is_open": False})
    elif ctx.triggered_id == "setprops-row-selection-popup" and selection:
        # Open the modal and display the selected row content
        content_to_display = "You selected " + ", ".join(
            [
                f"{s['make']} (model {s['model']} and price {s['price']})"
                for s in selection
            ]
        )
        set_props("setprops-row-selection-modal", {"is_open": True})
        set_props(
            "setprops-row-selection-modal-content", {"children": content_to_display}
        )


if __name__ == "__main__":
    app.run(debug=True)
