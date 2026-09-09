from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Base, engine
from models import Task


app = FastAPI(
    title="DevOps CI/CD API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False


tasks = {}
next_id = 1


@app.get("/")
def root():
    return {
        "message": "DevOps CI/CD API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/version")
def version():
    return {"version": app.version}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global next_id

    task_data = task.model_dump()
    task_data["id"] = next_id

    tasks[next_id] = task_data
    next_id += 1

    return task_data


@app.get("/tasks")
def list_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return tasks[task_id]


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    del tasks[task_id]

    return {"message": "Task deleted"}