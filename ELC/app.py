from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import random
from datetime import datetime
from pathlib import Path

app = FastAPI()

def generate_access_log():
    ips = ["192.168.1.1", "10.0.0.2", "172.16.0.3", "203.0.113.45"]
    methods = ["GET", "POST", "PUT", "DELETE"]
    urls = ["/", "/about", "/contact", "/products", "/api/data"]
    status_codes = [200, 301, 404, 500]
    referrers = ["-", "https://google.com", "https://example.com"]
    user_agents = [
        "Mozilla/5.0", 
        "AppleWebKit/537.36", 
        "Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    log_time = datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')
    return (
        f'{random.choice(ips)} - - [{log_time}] '
        f'"{random.choice(methods)} {random.choice(urls)} HTTP/1.1" '
        f'{random.choice(status_codes)} {random.randint(100, 5000)} '
        f'"{random.choice(referrers)}" "{random.choice(user_agents)}"'
    )

def generate_error_log():
    error_types = [
        "connect() failed", 
        "upstream timed out", 
        "client closed connection",
        "invalid host header"
    ]
    return (
        f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] "
        f"[error] {random.randint(1000, 9999)}#{random.randint(0, 10)}: "
        f"*{random.randint(10000, 99999)} {random.choice(error_types)}"
    )

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_access_log")
async def create_access_log():
    log_entry = generate_access_log()
    with open('/var/log/nginx/test-access.log', 'a') as f:
        f.write(log_entry + '\n')
    return {"message": "Access log created", "log_entry": log_entry}

@app.post("/generate_error_log")
async def create_error_log():
    log_entry = generate_error_log()
    with open('/var/log/nginx/test-error.log', 'a') as f:
        f.write(log_entry + '\n')
    return {"message": "Error log created", "log_entry": log_entry}
