from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation import rest_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rest_api.router, prefix="/api")
