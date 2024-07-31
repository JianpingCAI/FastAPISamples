import dash
import pandas as pd
from dash import callback, Input, Output, html, callback_context
import dash_mantine_components as dmc
import json

dash.register_page(__name__, path="/tasks")


def load_tasks():
    return pd.read_csv("data/tasks.csv")


layout = dmc.MantineProvider(
    [
        dmc.Title("Tasks", order=1),
        dmc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th(col)
                            for col in [
                                "Task Name",
                                "Description",
                                "Due Date",
                                "Status",
                                "Actions",
                            ]
                        ]
                    )
                ),
                html.Tbody(id="task-table-body"),
            ]
        ),
    ]
)


@callback(Output("task-table-body", "children"), Input("task-table-body", "id"))
def display_tasks(_):
    df = load_tasks()
    rows = []
    for _, row in df.iterrows():
        rows.append(
            html.Tr(
                [
                    html.Td(row["task_name"]),
                    html.Td(row["description"]),
                    html.Td(row["due_date"]),
                    html.Td(row["status"]),
                    html.Td(
                        [
                            dmc.Button(
                                "Complete",
                                id={"type": "complete-button", "index": str(row["id"])},
                            ),
                            dmc.Button(
                                "Delete",
                                id={"type": "delete-button", "index": str(row["id"])},
                            ),
                        ]
                    ),
                ]
            )
        )
    return rows


@callback(
    Output("task-table-body", "children", allow_duplicate=True),
    Input({"type": "complete-button", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def complete_task(n_clicks):
    if n_clicks is None or all(click is None for click in n_clicks):
        return dash.no_update
    df = load_tasks()
    # button_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    # task_id = json.loads(button_id)["index"]
    triggered_id = dash.callback_context.triggered_id
    if triggered_id is None:
        return dash.no_update
    task_id = triggered_id["index"]
    df.loc[df["id"] == int(task_id), "status"] = "Completed"
    df.to_csv("data/tasks.csv", index=False)
    return display_tasks(None)


@callback(
    Output("task-table-body", "children", allow_duplicate=True),
    Input({"type": "delete-button", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def delete_task(n_clicks):
    if n_clicks is None or all(click is None for click in n_clicks):
        return dash.no_update
    df = load_tasks()
    # button_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    # task_id = json.loads(button_id)["index"]
    triggered_id = dash.callback_context.triggered_id
    if triggered_id is None:
        return dash.no_update
    task_id = triggered_id["index"]
    df = df[df["id"] != int(task_id)]
    df.to_csv("data/tasks.csv", index=False)
    return display_tasks(None)
