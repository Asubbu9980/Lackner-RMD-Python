from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RMD Calculator API",
)

app.include_router(router)

# @app.get("/")
# def health_check():
#     return {"status": "checking if API is up and running"}