# it is entry point for the crawler service

from fastapi import FastAPI
import uvicorn
# for docker
# from .s3_upload import crawler
# from .s3_download import download
import sys
from .s3_upload import crawler
from .s3_download import download_and_insert_data
from .top5 import select_top5
import logging
import requests
import httpx
import boto3
import os

sys.path.append("../word_cloud")
# from .word_cloud_generator import generate_wordcloud_api
app = FastAPI()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')
s3 = boto3.client('s3',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)



def del_file_from_bucket(bucket_name, file_names):
    try:
        for file_name in file_names:
            response = s3.delete_object(Bucket=bucket_name, Key=file_name)
            print(response)
    except Exception as e:
        print(f"{file_name}파일을 삭제하는 중 오류가 발생했습니다: {e}")


@app.get("/crawling/")
async def create_upload_file():
    #try except block
    try:
        file_name= await crawler()
        #for docker container

        try:
            
            async with httpx.AsyncClient(timeout=1500) as client:
                #response=requests.get(f'http://localhost:80/processML/{file_name}')
                response = await client.get(f'http://models:80/processML/{file_name}')
                print("response",response)
                data=response.json()
                clustered_file_name=data["clustered_file_name"]
        except Exception as e:
            logging.error(f"Error processing file {file_name}: {e}")
            return {"message": f"Error processing file {file_name}"}
        
       #try except block
        try:
            print("clustered", clustered_file_name)
            download_and_insert_data(clustered_file_name)

        except(Exception) as e:
            logging.error(f"Error processing file {clustered_file_name}: {e}")
            return {"message": "File processed failed"}
        
        try:
            #for select top5 articles
            select_top5()
            print("File processed successfully")
        except Exception as e:
            logging.error(f"Error processing file {clustered_file_name}: {e}")
            return {"message": "File processed failed"}

        try:
            #for delete json file
            base, ext = os.path.splitext(file_name)  # Splitting the file name into base and extension

            del_file_from_bucket("aniop2023",[file_name, f"{base}_2{ext}", f"{base}_3{ext}"])
            print(f"messeage : {file_name} was deleted")
            return {"message": f"File {clustered_file_name} processed successfully"}

        except Exception as e:
            logging.error("error",e)
            return {"message": "File deleted processed failed"}

            
        
    except Exception as e:
        logging.error(f"Crawling failed: {e}")

        print("File processed failed", Exception)
        return {"message": "File processed failed"}
    