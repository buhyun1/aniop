from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import cluster
import pandas as pd
import tempfile
import shutil
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from model_loader import get_model


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
    get_model()  # 앱 시작 시 모델 로드

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.post("/cluster-news")
async def cluster_news(file: UploadFile = File(...)):
    print("Received file:", file.filename)  # 파일 수신 확인

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
    print("File saved to temporary path:", temp_file_path)  # 임시 파일 저장 경로 출력

    df = pd.read_excel(temp_file_path)
    print("Excel file loaded into DataFrame")  # 엑셀 파일 로딩 확인

    output_file_path = 'output_cluster.xlsx'  # 상대 경로 사용 권장
    saved_file_path = cluster.cluster_news_titles_and_save(df, output_file_path)
    print("Clustering completed and file saved:", saved_file_path)  # 클러스터링 완료 및 파일 저장 경로 출력

    return {"message": "File processed and saved", "file_path": saved_file_path}
