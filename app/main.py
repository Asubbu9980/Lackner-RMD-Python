from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="RMD Calculator API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "checking if API is up and running"}