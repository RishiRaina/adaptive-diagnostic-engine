from fastapi import FastAPI
from app.routes import test_routes

app = FastAPI(title="Adaptive Diagnostic Engine")

app.include_router(test_routes.router)

@app.get("/")
def root():
    return {"message":"Adaptive Diagnostic Engine Running"}