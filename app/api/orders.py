from fastapi import APIRouter
from pydantic import BaseModel
from app.worker.tasks import process_order, celery_app

router = APIRouter()

class OrderRequest(BaseModel):
    id: int

@router.post("/")
async def create_order(order: OrderRequest):
    task = process_order.delay(order.id)
    return {"task_id": task.id}

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    res = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": res.status,
        "result": res.result,
    }
