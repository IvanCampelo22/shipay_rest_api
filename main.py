
from fastapi import FastAPI
import logging
from loguru import logger 
import sys
from fastapi import FastAPI
import os   
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routers import api_router

app = FastAPI(title='Shipay-Challenge')
app.include_router(api_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
