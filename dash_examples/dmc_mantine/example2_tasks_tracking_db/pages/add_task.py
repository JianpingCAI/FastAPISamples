import dash
from dash import callback, Input, Output, State
import dash_mantine_components as dmc
from sqlalchemy.orm import Session
from utils.crud import create_task
from models.database import SessionLocal
from models.task import TaskCreate

dash.register_page(__name__, path="/add_task")

layout = dmc.MantineProvider(
    [
        dmc.Title("Add Task", order=1),
        dmc.TextInput(id="task-name", label="Task Name", placeholder="Enter task name"),
        dmc.Textarea(
            id="task-desc", label="Description", placeholder="Enter task description"
        ),
        dmc.DatePicker(id="task-due-date", label="Due Date"),
        dmc.Button("Submit", id="submit-task-button"),
        dmc.Text(id="add-task-output"),
    ]
)


@callback(
    Output("add-task-output", "children"),
    [Input("submit-task-button", "n_clicks")],
    [
        State("task-name", "value"),
        State("task-desc", "value"),
        State("task-due-date", "value"),
    ],
)
def add_task(n_clicks: int, name: str, desc: str, due_date: str) -> str:
    if n_clicks is None:
        return ""
    db: Session = SessionLocal()
    new_task = TaskCreate(task_name=name, description=desc, due_date=due_date)
    create_task(db, new_task)
    db.close()
    return f'Task "{name}" has been added.'
