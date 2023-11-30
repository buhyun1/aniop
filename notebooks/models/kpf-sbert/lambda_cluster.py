import json
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
from sklearn.cluster import AgglomerativeClustering
import hdbscan
import logging
import boto3
import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv('../.env')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')

#test env loading
print("aws_access_key_id :",aws_access_key_id)
print("aws_secret_access_key :",aws_secret_access_key)
print("region_name :",region_name)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def load_model(model_path):
    # S3에서 모델 다운로드
    # 모델 로드
    model = SentenceTransformer(model_path)
    return model

# Function to process UMAP
def umap_process(corpus_embeddings, n_components=5):
    return umap.UMAP(n_neighbors=15, n_components=n_components, metric='cosine').fit_transform(corpus_embeddings)

def cluster_texts_by_category(model, df, category_col='Category', text_col='Title'):
    clustered_data = []
    for category in df[category_col].unique():
        category_df = df[df[category_col] == category]
        if not category_df.empty:
            embeddings = model.encode(category_df[text_col].tolist())
            reduced_embeddings = umap_process(embeddings)
            if reduced_embeddings.shape[0] < 2:
                # Skip if the number of samples is less than 2
                print(f'Skipping category {category} due to insufficient number of samples.')
                continue  # 샘플 개수가 2개 미만인 경우 스킵
            # Agglomerative Clustering
            agg_cluster = AgglomerativeClustering(n_clusters=None, distance_threshold=0.3)
            agg_labels = agg_cluster.fit_predict(reduced_embeddings)
            # HDBSCAN Clustering
            hdbscan_cluster = hdbscan.HDBSCAN(min_cluster_size=3, gen_min_span_tree=True)
            hdbscan_labels = hdbscan_cluster.fit_predict(reduced_embeddings)
            # Add results to DataFrame
            category_df['Agglomerative_Cluster'] = agg_labels
            category_df['HDBSCAN_Cluster'] = hdbscan_labels
            clustered_data.append(category_df)
            
    return pd.concat(clustered_data)

def lambda_cluster(event):

    try:
    # S3 클라이언트 초기화
        s3 = boto3.client('s3', 
                        region_name=region_name, 
                        aws_access_key_id=aws_access_key_id, 
                        aws_secret_access_key=aws_secret_access_key)
        logger.info("Initialized S3 client.")
    except Exception as e:
        logger.error(f"Error initializing S3 client: {e}")
        raise e

    try:
        # S3 버킷과 객체 키 추출
        bucket_name= event['bucket']
        object_key = event['input_file']
        out_object_key = event['output_file']
        logger.info(f"Bucket: {bucket_name}, Input File: {object_key}, Output File: {out_object_key}")

        # S3에서 입력 파일 읽기
        input_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        input_data = json.loads(input_obj['Body'].read().decode('utf-8'))
        logger.info(f"Successfully read input file from S3: {object_key}")
    except Exception as e:
        logger.error(f"Error reading from S3: {e}")
        raise e
    # 출력 데이터 준비
    outdata = input_data.copy()
    
    #json to dataframe
    df = pd.DataFrame(input_data['news'])
    data=df
    # local_test 모델 로드
    model_path = "../models/kpf-sbert/model_file"
    
    #for docker container
    #model_path = "models/kpf-sbert/model_file"
    model = load_model(model_path)

    # 카테고리 별 클러스터링 수행
    logger.info("Performing clustering by category.")
    clustered_df = cluster_texts_by_category(model, df)


    # 클러스터링 결과를 JSON으로 변환
    logger.info("Converting results to JSON.")
    clustered_json = clustered_df.to_json(orient='records', force_ascii=False)
    print("clustered_json :",clustered_json)  # 출력된 결과 확인

    outdata['news'] = json.loads(clustered_json)

   

    # 결과 파일을 S3에 업로드
    output_json = json.dumps(outdata, ensure_ascii=False)


    # S3에 결과 파일 쓰기
    s3.put_object(Body=output_json, Bucket=bucket_name, Key=out_object_key)

    return {
        'statusCode': 200,
        'body': 'File processed and uploaded successfully.'
    }
# Example event data
test_event = {'bucket': 'aniop2023', 
                  'input_file': 'manual_predicted_news_articles.json', 
                  'output_file': 'manual_predicted_news_articles.json'}

if __name__ == "__main__":
    result=lambda_handler(test_event)
    print("clustered success")
    print(result)
