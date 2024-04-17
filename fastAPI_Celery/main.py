from fastapi import FastAPI
from tasks.worker import celery_app
from http.client import HTTPException
from celery.result import AsyncResult

app = FastAPI()


@app.post("/start-task/")
async def start_task():
    task = celery_app.send_task("worker.long_running_task", args=[20])
    return {"message": "Task started", "task_id": task.id}


@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == "PROGRESS":
        return {"status": task_result.state, "progress": task_result.info}
    elif task_result.state == "FAILURE":
        return {"status": task_result.state, "error": task_result.info}
    else:
        return {
            "status": task_result.state,
            "result": task_result.result if task_result.ready() else "Not ready",
        }


@app.post("/cancel-task/{task_id}")
async def cancel_task(task_id: str):
    celery_app.control.revoke(task_id, terminate=True)
    return {"message": "Task cancellation requested", "task_id": task_id}
