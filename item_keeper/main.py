from fastapi import FastAPI
from fastapi import Query

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items")
def get_items(skip: int = Query(0), limit: int = Query(10)):
    all_items = ["item1", "item2", "item3", "item4", "item5"]
    return {"items": all_items[skip : skip + limit]}

@app.get("/items_by_id")
def get_items_by_id():
    return {"items": ["item1", "item2", "item3"]}