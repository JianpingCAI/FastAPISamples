import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Initialize the Dash app with external MathJax script
app = dash.Dash(
    __name__,
    external_scripts=[
        {
            "src": "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"
        }
    ],
)

# Define the layout
app.layout = html.Div(
    [
        dcc.Markdown(
            """
            ## MathJax in Dash

            Here is an equation rendered with MathJax:

            $$ E = mc^2 $$
            """,
            id="mathjax-output",
        ),
        dcc.Input(
            id="math-input", type="text", value="E = mc^2", style={"width": "100%"}
        ),
        html.Button("Update Equation", id="update-button"),
        dcc.Store(id="mathjax-store"),  # Hidden Store to trigger MathJax re-render
    ]
)


# Callback to update the MathJax content dynamically
@app.callback(
    Output("mathjax-output", "children", allow_duplicate=True),
    Output("mathjax-store", "data", allow_duplicate=True),
    Input("update-button", "n_clicks"),
    State("math-input", "value"),
    prevent_initial_call=True,
)
def update_mathjax(n_clicks, input_value):
    # Update Markdown with new equation
    updated_markdown = f"""
    ## MathJax in Dash

    Here is an equation rendered with MathJax:

    $$ {input_value} $$
    """
    # Return updated Markdown and trigger data change
    return updated_markdown, input_value


# JavaScript code to re-render MathJax after Dash updates the DOM
app.clientside_callback(
    """
    function(children) {
        console.log("clientside callback: " + children);
        if (window.MathJax) {
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]); // Re-render MathJax content
        }
        return children; // Return children to prevent any data flow interruption
    }
    """,
    Output("mathjax-output", "children"),  # Directly output to the Markdown component
    Input("mathjax-store", "data"),  # Trigger on data change from callback
    prevent_initial_call=True,
)

# Delay initial rendering of MathJax (if necessary)
app.clientside_callback(
    """
    function() {
        console.log("clientside callback called.");
        if (window.MathJax && !window.mathJaxRendered) {
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
            window.mathJaxRendered = true; // Set a flag to prevent repeated calls
        }
    }
    """,
    Output("mathjax-store", "data"),
    Input("mathjax-store", "data"),
    prevent_initial_call=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
