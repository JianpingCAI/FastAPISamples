from dash import Dash, dcc, html, Input, Output, Patch, MATCH, ALLSMALLER, callback
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    [
        html.Button("Add Filter", id="add-filter-ex3-btn", n_clicks=0),
        html.Div(id="container-ex3-div", children=[]),
    ]
)


@callback(
    Output("container-ex3-div", "children"), Input("add-filter-ex3-btn", "n_clicks")
)
def display_dropdowns(n_clicks):
    patched_children = Patch()
    patched_children.append(
        html.Div(
            [
                dcc.Dropdown(
                    df["country"].unique(),
                    df["country"].unique()[n_clicks],
                    id={"type": "filter-dd-ex3", "index": n_clicks},
                ),
                html.Div(id={"type": "output-div-ex3", "index": n_clicks}),
            ]
        )
    )
    return patched_children


@callback(
    Output({"type": "output-div-ex3", "index": MATCH}, "children"),
    Input({"type": "filter-dd-ex3", "index": MATCH}, "value"),
    Input({"type": "filter-dd-ex3", "index": ALLSMALLER}, "value"),
)
def display_output(matching_value, previous_values):
    previous_values_in_reversed_order = previous_values[::-1]
    all_values = [matching_value] + previous_values_in_reversed_order

    dff = df[df["country"].str.contains("|".join(all_values))]
    avgLifeExp = dff["lifeExp"].mean()

    # Return a slightly different string depending on number of values
    if len(all_values) == 1:
        return html.Div(
            "{:.2f} is the life expectancy of {}".format(avgLifeExp, matching_value)
        )
    elif len(all_values) == 2:
        return html.Div(
            "{:.2f} is the average life expectancy of {}".format(
                avgLifeExp, " and ".join(all_values)
            )
        )
    else:
        return html.Div(
            "{:.2f} is the average life expectancy of {}, and {}".format(
                avgLifeExp, ", ".join(all_values[:-1]), all_values[-1]
            )
        )


if __name__ == "__main__":
    app.run(debug=True)
