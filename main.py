from fastapi import FastAPI
from webhook import router as webhook_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "WaxPrep is running"}

app.include_router(webhook_router)
