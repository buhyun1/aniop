from soynlp.noun import LRNounExtractor_v2
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

# 불용어 목록
stopwords = set(['기자', '연합뉴스', '에서', '이다', '것이다', '있다', '등', '이', '그', '저'])

def extract_titles_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        text = ''
        for article in data['news']:
            if 'Title' in article and article['Title']:
                text += article['Title'] + ' '
        return text

def generate_wordcloud(text):
    # 명사 추출기 초기화 및 학습
    noun_extractor = LRNounExtractor_v2(verbose=True)
    nouns = noun_extractor.train_extract(text.split())

    # 불용어 제거 및 빈도수 추출
    filtered_nouns = {word: score.frequency for word, score in nouns.items() if word not in stopwords and len(word) > 1}

    # 워드 클라우드 생성
    wordcloud = WordCloud(
        font_path='malgun.ttf',  # 한글 폰트 경로
        width=800,
        height=400,
        background_color='white'
    ).generate_from_frequencies(filtered_nouns)

    return wordcloud


# 데이터 추출
text = extract_titles_from_file('data_test_labeled.json')

# 워드 클라우드 생성 및 시각화
wordcloud = generate_wordcloud(text)

# 워드 클라우드 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()


## S3 업로드
import os
import boto3
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime
from PIL import Image

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# 환경 변수에서 값 가져오기
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def upload_to_s3(bucket_name, image_name, image_data):
    # S3 클라이언트 생성
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # 이미지를 S3 버킷에 업로드
    s3_client.put_object(
        Bucket=bucket_name, 
        Key=image_name, 
        Body=buffer, 
        ContentType='image/png'
    )

    print(f"Image uploaded to S3: {bucket_name}/{image_name}")

# 워드 클라우드 이미지 생성 및 바이트 버퍼로 저장
wordcloud_image = generate_wordcloud(text)
buffer = BytesIO()
wordcloud_image.to_image().save(buffer, format="PNG")
buffer.seek(0)
image_data = buffer.getvalue()

# 이미지 파일 이름 설정 (오늘 날짜 포함)
current_date = datetime.now().strftime('%Y%m%d')
image_file_name = f'wordcloud_{current_date}.png'

# S3에 이미지 업로드
upload_to_s3(S3_BUCKET_NAME, image_file_name, image_data)


## Flask 애플리케이션으로 변환
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/generate-wordcloud', methods=['GET'])
def generate_wordcloud_api():
    # 데이터 추출 및 워드 클라우드 생성
    text = extract_titles_from_file('data_test_labeled.json')
    wordcloud_image = generate_wordcloud(text)

    # 이미지 파일 이름 설정 (오늘 날짜 포함)
    current_date = datetime.now().strftime('%Y%m%d')
    image_file_name = f'wordcloud_{current_date}.png'

    # 바이트 버퍼에 이미지 저장
    buffer = BytesIO()
    wordcloud_image.to_image().save(buffer, format="PNG")
    buffer.seek(0)
    image_data = buffer.getvalue()

    # S3에 이미지 업로드
    upload_to_s3(S3_BUCKET_NAME, image_file_name, image_data)

    # S3 이미지 URL 반환
    image_url = f'https://{S3_BUCKET_NAME}.s3.amazonaws.com/{image_file_name}'
    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    app.run(debug=False)
