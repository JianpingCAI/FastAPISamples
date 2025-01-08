from typing import Iterable
from dash import Dash, html, dcc, Input, Output, State
import dash_mantine_components as dmc

# Initialize the Dash app
app = Dash(__name__)
server = app.server

# Define the layout with input fields, buttons, output divs, and a Notifications provider
app.layout = dmc.MantineProvider(
    [
        dcc.Input(id="input1", type="number", placeholder="Enter a number"),
        dcc.Input(id="input2", type="number", placeholder="Enter another number"),
        html.Button("Calculate Sum and Product", id="calculate-button"),
        html.Button("Divide", id="divide-button"),
        dmc.NotificationProvider(position="top-right"),
        html.Div(id="notifications-container"),
        html.Div(id="sum-output"),
        html.Div(id="product-output"),
        html.Div(id="division-output"),
    ]
)


# Helper function for reusable exception handling with notifications
def handle_with_notifications(
    callback_logic: callable, success_message: str = None, default_outputs: list = None
) -> list:
    notifications = []
    try:
        # Run the main callback logic and collect all intended outputs
        result_outputs = callback_logic()

        # Ensure result_outputs is always a list
        if (
            isinstance(result_outputs, Iterable)
            and not isinstance(result_outputs, str)
            and not isinstance(result_outputs, list)
        ):
            # Wrap non-iterable or string output in a list
            result_outputs = list(result_outputs)
    except Exception as e:
        notifications.append(f"Error: {str(e)}")
        result_outputs = default_outputs if default_outputs is not None else []
    
    if success_message:
        notifications.append(success_message)
    
    # Handle notifications (this part is assumed and should be implemented)
    # for notification in notifications:
    #     dmc.show_notification(notification)
    
    return result_outputs


# Callback for calculating sum and product
@app.callback(
    Output("notifications-container", "children", allow_duplicate=True),
    Output("sum-output", "children"),
    Output("product-output", "children"),
    Input("calculate-button", "n_clicks"),
    State("input1", "value"),
    State("input2", "value"),
    prevent_initial_call=True,
)
def calculate_sum_and_product(n_clicks, input1, input2):
    def callback_logic():
        if input1 is None or input2 is None:
            raise ValueError("Both inputs are required.")
        # Perform the operations
        return f"Sum: {input1 + input2}", f"Product: {input1 * input2}"

    # Updated usage of handle_with_notifications with None as default output placeholders
    return handle_with_notifications(
        callback_logic,
        success_message="Calculation Successful",
        default_outputs=[
            "Sum could not be calculated.",
            "Product could not be calculated.",
        ],
    )


# Callback for division calculation
@app.callback(
    Output("notifications-container", "children", allow_duplicate=True),
    Output("division-output", "children"),
    Input("divide-button", "n_clicks"),
    State("input1", "value"),
    State("input2", "value"),
    prevent_initial_call=True,
)
def calculate_division(n_clicks, input1, input2):
    def callback_logic():
        if input1 is None or input2 is None:
            raise ValueError("Both inputs are required.")
        # Perform division
        return (f"Division: {input1 / input2}",)

    # Simplified default output setting
    return handle_with_notifications(
        callback_logic,
        success_message="Division Successful",
        default_outputs=["Division could not be calculated."],
    )


if __name__ == "__main__":
    app.run_server(debug=True)
