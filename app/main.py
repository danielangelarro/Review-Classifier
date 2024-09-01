from fastapi import FastAPI
from app.presentation import rest_api

# Entry point for the API
app = FastAPI()

app.include_router(rest_api.router, prefix="/api")