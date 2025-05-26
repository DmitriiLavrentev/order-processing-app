from celery import Celery, current_task
import os, time

broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "order_tasks",
    broker=broker_url,
    backend=backend_url,
)

@celery_app.task(bind=True)  # Обратите внимание на bind=True для доступа к current_task
def process_order(self, order_id: int):
    # Устанавливаем начальный статус
    self.update_state(state='PROGRESS', meta={'status': 'processing', 'order_id': order_id})
    
    print(f"[Worker] Processing order {order_id}...")
    
    # Имитация работы - этап 1
    time.sleep(5)
    self.update_state(state='PROGRESS', meta={'status': 'halfway', 'order_id': order_id})
    print(f"[Worker] Halfway through order {order_id}...")
    
    # Имитация работы - этап 2
    time.sleep(10)
    
    print(f"[Worker] Done processing order {order_id}.")
    return {"status": "success", "order_id": order_id}