# it is entry point for the crawler service

from fastapi import FastAPI
import uvicorn
# for docker
# from .s3_upload import crawler
# from .s3_download import download
import sys
from s3_upload import crawler
from s3_download import download
from top5 import select_top5
import logging
import requests

sys.path.append("../word_cloud")
from word_cloud_generater import word_cloud
app = FastAPI()

@app.get("/crawling/")
async def create_upload_file():
    #try except block
    try:
        file_name= await crawler()
        #for docker container
        #requests.get(f'http://models:80/processML/{file_name}')
        #for local

        try:
            response=requests.get(f'http://localhost:80/processML/{file_name}')
            data=response.json()
            clustered_file_name=data["clustered_file_name"]
        except Exception as e:
            logging.error(f"Error processing file {file_name}: {e}")
            return {"message": f"Error processing file {file_name}"}
        
       #try except block
        try:
            print("clustered", clustered_file_name)
            download(clustered_file_name)

        except(Exception) as e:
            logging.error(f"Error processing file {clustered_file_name}: {e}")
            return {"message": "File processed failed"}
        
        try:
            #for select top5 articles
            select_top5()
            print("File processed successfully")
            return {"message": f"File {clustered_file_name} processed successfully"}
        except Exception as e:
            logging.error(f"Error processing file {clustered_file_name}: {e}")
            return {"message": "File processed failed"}

    except Exception as e:
        logging.error(f"Crawling failed: {e}")

        print("File processed failed", Exception)
        return {"message": "File processed failed"}
    