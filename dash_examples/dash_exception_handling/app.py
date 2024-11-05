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
    callback_logic, success_message=None, default_outputs=None
):
    notifications = []
    try:
        # Run the main callback logic and collect all intended outputs
        result_outputs = callback_logic()

        # Add a success notification if specified
        if success_message:
            notifications.append(
                dmc.Notification(
                    title="Success",
                    action="show",
                    message=success_message,
                    color="green",
                    autoClose=3000,
                )
            )
        # Return notifications and callback result
        return [notifications] + list(result_outputs)

    except ZeroDivisionError:
        notifications.append(
            dmc.Notification(
                title="Error",
                message="Cannot divide by zero!",
                action="show",
                color="red",
                autoClose=5000,
            )
        )
    except ValueError as e:
        notifications.append(
            dmc.Notification(
                title="Input Error",
                message=str(e),
                action="show",
                color="orange",
                autoClose=5000,
            )
        )
    except Exception as e:
        notifications.append(
            dmc.Notification(
                title="Unexpected Error",
                message=f"An error occurred: {str(e)}",
                action="show",
                color="red",
                autoClose=5000,
            )
        )

    # Return notifications with default outputs or None if no default outputs specified
    return [notifications] + (
        default_outputs if default_outputs else [None] * len(result_outputs)
    )


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
