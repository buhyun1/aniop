from flask import Flask, request, jsonify
import json
from soynlp.noun import LRNounExtractor_v2
from wordcloud import WordCloud
from io import BytesIO
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv

# 불용어 목록
stopwords = set(['기자', '연합뉴스', '에서', '이다', '것이다', '있다', '등', '이', '그', '저'])

# JSON 데이터에서 제목 추출
def extract_titles_from_json(json_data):
    text = ''
    for article in json_data['news']:
        if 'Title' in article and article['Title']:
            text += article['Title'] + ' '
    return text

# 워드 클라우드 생성 함수
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



# .env 파일에서 환경 변수 불러오기
load_dotenv()

# 환경 변수에서 값 가져오기
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def upload_to_s3(bucket_name, image_name, buffer):
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

# Flask 애플리케이션 설정
app = Flask(__name__)

@app.route('/generate-wordcloud', methods=['POST'])
def generate_wordcloud_api():
    # JSON 데이터를 요청 본문에서 불러옴
    data = request.json

    # 제공된 JSON 데이터를 이용하여 텍스트 추출
    text = extract_titles_from_json(data)

    # 워드 클라우드 생성
    wordcloud = generate_wordcloud(text)

    # 바이트 버퍼에 이미지 저장
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format="PNG")
    buffer.seek(0)

    # S3에 이미지 업로드
    current_date = datetime.now().strftime('%Y%m%d')
    image_file_name = f'wordcloud_{current_date}.png'
    upload_to_s3(os.getenv('S3_BUCKET_NAME'), image_file_name, buffer)

    # S3 이미지 URL 반환
    image_url = f'https://{os.getenv(S3_BUCKET_NAME)}.s3.amazonaws.com/{image_file_name}'
    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=False)