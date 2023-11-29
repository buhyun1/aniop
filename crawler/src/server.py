# it is entry point for the crawler service

from fastapi import FastAPI
import uvicorn
# for docker
# from .s3_upload import crawler
# from .s3_download import download

from s3_upload import crawler
from s3_download import download
import logging
import requests

app = FastAPI()

@app.get("/crawling/")
async def create_upload_file():
    #try except block
    try:
        file_name= await crawler()
        #for docker container
        #requests.get(f'http://models:80/processML/{file_name}')
        #for local
        response=requests.get(f'http://localhost:80/processML/{file_name}')
        print(response.json())
        return {"message": "File processed successfully"}
    except Exception as e:
        logging.error(f"Crawling failed: {e}")

        print("File processed failed", Exception)
        return {"message": "File processed failed"}
    
@app.get("/download/{clustered_file_name}")
async def download_file(clustered_file_name: str):
    #try except block
    try:
        await download(clustered_file_name)

        return {"message": "File processed successfully"}
    except(Exception):
        print("File processed failed", Exception)
        return {"message": "File processed failed"}