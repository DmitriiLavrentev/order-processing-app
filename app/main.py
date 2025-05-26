from fastapi import FastAPI
from app.api import orders
from contextlib import asynccontextmanager
import redis.asyncio as redis
from prometheus_fastapi_instrumentator import Instrumentator

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = redis.from_url("redis://redis:6379/0", encoding="utf-8", decode_responces=True)
    yield
    await app.state.redis.close()

app = FastAPI(title="Order Processing Service", lifespan=lifespan)

app.include_router(orders.router, prefix="/orders", tags=["orders"])

Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Order Processing Service is running"}