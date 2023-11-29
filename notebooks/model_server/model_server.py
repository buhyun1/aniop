from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from .check_s3 import main
import sys
import requests
app = FastAPI()

# Add CORSMiddleware to your FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
async def startup_event():
    print("startup_event")
    return("startup_event")



@app.get("/processML/{file_name}")
async def process_file(file_name: str):
    try:
        await main(file_name)
        print("check_s3.py 실행")

        return {"message": f"File {file_name} processed successfully"}
        await requests.get('http://crawler:8080/download/')
        print("download.py 실행")

    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")
        return {"message": f"Error processing file {file_name}"}