# it is entry point for the crawler service

from fastapi import FastAPI
import uvicorn
from .s3_upload import crawler
from .s3_download import download
import logging
import requests

app = FastAPI()

@app.get("/crawling/")
async def create_upload_file():
    #try except block
    try:
        file_name=await crawler()
        await requests.get(f'http://models:80/processML/{file_name}')
        return {"message": "File processed successfully"}
    except Exception as e:
        logging.error(f"Crawling failed: {e}")

        print("File processed failed", Exception)
        return {"message": "File processed failed"}
    
@app.get("/download/")
async def download_file():
    #try except block
    try:
        await download()

        return {"message": "File processed successfully"}
    except(Exception):
        print("File processed failed", Exception)
        return {"message": "File processed failed"}