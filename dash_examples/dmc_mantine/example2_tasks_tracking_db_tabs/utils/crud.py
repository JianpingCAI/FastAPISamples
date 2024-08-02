from sqlalchemy.orm import Session
from typing import List

from models.task import Task, TaskCreate, TaskUpdate


def get_tasks(db: Session) -> List[Task]:
    return db.query(Task).all()


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(
        task_name=task.task_name,
        description=task.description,
        due_date=task.due_date,
        status="Pending",
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task_status(db: Session, task_id: int, status: str) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
