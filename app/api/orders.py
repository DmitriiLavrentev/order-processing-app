from fastapi import APIRouter, Request
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
async def get_status(task_id: str, request: Request):
    redis = request.app.state.redis

    # Попытка получить результат из кеша Redis
    cached_result = await redis.get(task_id)
    if cached_result is not None:
        return {
            "task_id": task_id,
            "status": "CACHED",
            "result": cached_result,
        }

    # Если результата в Redis нет — берём из Celery
    res = celery_app.AsyncResult(task_id)
    
    # Если задача завершена, кладём в Redis
    if res.ready():
        await redis.set(task_id, str(res.result), ex=300)  # TTL = 300 сек (5 мин)

    return {
        "task_id": task_id,
        "status": res.status,
        "result": res.result,
    }
