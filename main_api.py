from fastapi import FastAPI
from scraper_module import scrape_vinted_api

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/search")
async def search(params: dict):
    return await scrape_vinted_api(params)
