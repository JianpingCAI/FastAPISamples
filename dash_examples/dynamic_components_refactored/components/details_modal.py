# Components should not define callbacks within their classes because callbacks are a part of the overall application logic,
# not specific to individual components. Defining callbacks within components makes it difficult to reuse components across
# different applications.
#
# Components should be self-contained and only provide a single functionality. By not defining callbacks within components,
# we can reuse the same component across different applications without having to rewrite the callback logic.


from dash import html, Input, Output, MATCH, callback
import dash_bootstrap_components as dbc


class DetailsModalComponent:
    def __init__(self, modal_id, selected_row):
        self.modal_id = modal_id
        self.selected_row = selected_row
        self.component = self._create_component()

    def _create_component(self) -> dbc.Modal:
        # Create a modal dynamically based on the selected row data
        return dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(f"Details for {self.selected_row['make']}")
                ),
                dbc.ModalBody(
                    [
                        html.P(f"Model: {self.selected_row['model']}"),
                        html.P(f"Price: ${self.selected_row['price']:,}"),
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
            id=self.modal_id,
            is_open=True,  # Open the modal
        )

    def get_component(self) -> dbc.Modal:
        return self.component


# Callback to close the modal
@callback(
    Output({"type": "dynamic-modal", "index": MATCH}, "is_open"),
    Input({"type": "close-modal-button", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,  # Prevents callback from running on initial page load
)
def close_modal(n_clicks):
    # Check if the modal exists to avoid triggering errors
    if n_clicks:
        return False  # Close the modal
    return True
