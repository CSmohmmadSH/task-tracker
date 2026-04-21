from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from typing import List
import os
import uuid

# Create the FastAPI app
app = FastAPI(
    title="Task Tracker API",
    description="A simple task manager built for learning Kubernetes",
    version=os.environ.get("APP_VERSION", "v1")
)

# Prometheus metrics
tasks_created_total = Counter(
    "tasks_created_total",
    "Total number of tasks created"
)
tasks_deleted_total = Counter(
    "tasks_deleted_total",
    "Total number of tasks deleted"
)
requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["endpoint"]
)

# In-memory "database" — simple dict for now
# Day 3 replaces this with PostgreSQL
tasks_db = {}


# Data models
class TaskCreate(BaseModel):
    title: str
    description: str = ""


class Task(BaseModel):
    id: str
    title: str
    description: str
    completed: bool = False


# Routes

@app.get("/")
def root():
    requests_total.labels(endpoint="/").inc()
    return {
        "app": "Task Tracker",
        "version": os.environ.get("APP_VERSION", "v1"),
        "message": "Welcome! Try /tasks to see your tasks."
    }


@app.get("/health")
def health():
    """Kubernetes will hit this to check if the pod is healthy"""
    return {"status": "healthy"}


@app.get("/tasks", response_model=List[Task])
def list_tasks():
    requests_total.labels(endpoint="/tasks").inc()
    return list(tasks_db.values())


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    requests_total.labels(endpoint="/tasks").inc()
    task_id = str(uuid.uuid4())[:8]
    new_task = Task(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=False
    )
    tasks_db[task_id] = new_task
    tasks_created_total.inc()
    return new_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    requests_total.labels(endpoint="/tasks/{id}").inc()
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    tasks_deleted_total.inc()
    return None


@app.get("/metrics")
def metrics():
    """Prometheus scrapes this endpoint to collect metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)