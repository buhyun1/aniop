from flask import Flask, request, jsonify
from io import BytesIO
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv

from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

load_dotenv()

# 환경 변수에서 값 가져오기
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = 'aniop2023'

# 불용어 목록
stopwords = set(['스마트', '건설', '건설업', '사고', '사망', '처벌', '기술', '조선업', '조선', '선박', '이슈', '기업', '산업', '재해', '중대', '안전', '기자', '연합뉴스', '에서', '이다', '것이다', '있다', '등', '이', '그', '저', '시장', '동향'])

# JSON 데이터에서 제목 추출
def extract_titles_by_category(json_data, category_id):
    text = ''
    for article in json_data:
        if 'Title' in article and article['Title'] and article['CategoryID'] == category_id:
            text += article['Title'] + ' '
    
    # 불용어 제거 후 남아있는 단어가 없으면 'No text available'을 반환
    if not text:
        return 'No text available'
    
    return text

def generate_wordcloud(text, category_id):
    okt = Okt()  # Okt 형태소 분석기 인스턴스 생성

    # 원본 텍스트가 비어 있다면 워드 클라우드 생성하지 않음
    if not text:
        return None

    # 명사 추출 및 불용어 제거
    nouns = [noun for noun in okt.nouns(text) if noun not in stopwords and len(noun) > 1]
    word_counts = Counter(nouns)

    # 워드 클라우드 생성
    wordcloud = WordCloud(
        font_path='./malgun.ttf',  # 한글 폰트 경로
        width=800,
        height=400,
        background_color='white'
    ).generate_from_frequencies(word_counts)

    return wordcloud

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
    s3_image_urls = []

    # 각 카테고리별로 워드 클라우드 생성 및 S3에 업로드
    for category_id in range(4):
        # 제공된 JSON 데이터를 이용하여 텍스트 추출
        text = extract_titles_by_category(data, category_id)

        # 워드 클라우드 생성
        wordcloud = generate_wordcloud(text, category_id)

        # 바이트 버퍼에 이미지 저장
        buffer = BytesIO()
        wordcloud.to_image().save(buffer, format="PNG")
        buffer.seek(0)

        # S3에 이미지 업로드
        current_date = datetime.now().strftime('%Y%m%d')
        image_file_name = f'wordcloud_category_{category_id}_{current_date}.png'
        upload_to_s3('aniop2023', image_file_name, buffer)

        # 업로드된 이미지의 S3 링크 출력
        image_url = f'https://{S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image_file_name}'
        s3_image_urls.append(image_url)
        print(s3_image_urls)

    return jsonify({'message': 'Word Clouds generated and uploaded to S3', 'image_urls': s3_image_urls})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
