from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.vector import router as vector_router

def create_app():
    app = FastAPI()
    app.include_router(health_router)
    app.include_router(vector_router)
    return app

app = create_app()