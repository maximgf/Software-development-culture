import logging
import logging.config
from pathlib import Path
from fastapi import FastAPI, Request

# Настройка пути для логов
LOG_DIR = Path("/var/log/fastapi")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

# Конфигурация логирования
logging.config.fileConfig('logging.conf', defaults={'logfilename': str(LOG_FILE)})
logger = logging.getLogger("fastapi")

app = FastAPI()

@app.get("/")
async def root(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"Request from IP: {client_ip} to endpoint: /")
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"Request from IP: {client_ip} to endpoint: /items/{item_id}")
    return {"item_id": item_id}