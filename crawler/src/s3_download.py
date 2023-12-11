import os
from dotenv import load_dotenv
import subprocess
import json
import mysql.connector
import boto3
from datetime import datetime, timedelta

def download_and_insert_data(clustered_file_name):
    print("clustered_file_name:", clustered_file_name, "with download_and_insert_data function")

    # .env 파일 로드
    load_dotenv()

    # 추가: AWS 자격 증명 및 S3 설정
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket_name = 'aniop2023'

    # Create an S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Download the file from S3
    local_filename = os.path.join('/app', 'src', 'data', clustered_file_name)
    print("local_file_name", local_filename)
    try:
        s3_client.download_file(bucket_name, clustered_file_name, local_filename)
        print("S3 file download complete")
    except Exception as e:
        print(f"Error downloading S3 file: {str(e)}")
        return

    # # 추가: AWS CLI를 사용하여 S3 객체 다운로드
    
    # try:
    #     subprocess.run(['aws', 's3', 'cp', f's3://{bucket_name}/{clustered_file_name}', './crawler/src/data/'], check=True, env={
    #         'AWS_ACCESS_KEY_ID': aws_access_key_id,
    #         'AWS_SECRET_ACCESS_KEY': aws_secret_access_key
    #     })
    #     # 다운로드 성공 메시지 출력
    #     print("S3 파일 다운로드 완료")
    # except subprocess.CalledProcessError as e:
    #     # 다운로드 실패 메시지 출력
    #     print(f"S3 파일 다운로드 오류: {str(e)}")
    #     return

    # JSON 파일 다운로드 경로 설정
    #down_name = f'src/data/{clustered_file_name}'
    down_name = f'/app/src/data/{clustered_file_name}'
    # JSON 파일 파싱 및 데이터 추출
    
    data = []
    try:
        with open(down_name, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(f"JSON 파일 파싱 오류: {str(e)}")
        return

    # 환경 변수에서 연결 정보 가져오기
    host = os.getenv('MYSQL_HOST')
    port = int(os.getenv('MYSQL_PORT'))
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')

    try:
        # MySQL 데이터베이스에 연결 시도
        conn = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database,
            port=port
        )

        # 연결 성공 메시지 출력
        print("MySQL 데이터베이스에 연결되었습니다.")

        # 데이터베이스 작업 수행
        cursor = conn.cursor()

        # JSON 데이터를 MySQL 데이터베이스에 삽입하는 코드
        for item in data['news']:
            title = item['Title']
            link = item['Link']
            CategoryID = item['Category']
            DailyRelatedArticleCount = item['HDBSCAN_Cluster']
            # INSERT 쿼리 실행
            insert_query = "INSERT INTO Articles (Title, ArticleLink, CategoryID, DailyRelatedArticleCount) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (title, link, CategoryID, DailyRelatedArticleCount))

        # 변경 사항을 커밋
        conn.commit()

        # 연결 종료
        cursor.close()
        conn.close()
        print("데이터베이스에 데이터 삽입 완료")
    except mysql.connector.Error as err:
        # 연결 실패 또는 데이터베이스 작업 오류 메시지 출력
        print(f"MySQL 데이터베이스 오류: {err}")

def main():
    # Example clustered file name
    clustered_file_name = "20231207_combined_news_3.json"

    # Call the download_and_insert_data function with the clustered file name
    download_and_insert_data(clustered_file_name)

if __name__ == "__main__":
    main()
