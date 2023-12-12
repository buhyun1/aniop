from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

# 형태소 분석기 초기화
okt = Okt()

# 불용어 목록
stopwords = set(['스마트', '건설', '건설업', '사고', '사망', '처벌', '기술', '조선업', '조선', '선박', '이슈', '기업', '산업', '재해', '중대', '안전', '기자', '연합뉴스', '에서', '이다', '것이다', '있다', '등', '이', '그', '저', '시장', '동향'])

def extract_titles_by_category(json_data, category_id):
    text = ''
    for article in json_data:
        if 'Title' in article and article['Title'] and article['CategoryID'] == category_id:
            text += article['Title'] + ' '
    return text

def generate_wordcloud(text, category_id):
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

# JSON 파일 경로 지정
json_file_path = 'C:/Users/Ahn Yehyeon/Desktop/2023-1/aniop/notebooks/data/processed/musma_news_data.json'

# JSON 파일에서 데이터 읽어오기
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 각 카테고리별로 워드 클라우드 생성 및 파일로 저장
for category_id in range(4):
    text = extract_titles_by_category(data, category_id)
    wordcloud = generate_wordcloud(text, category_id)

    # 파일명 지정
    image_file_name = f'wordcloud_{category_id}.png'
    
    # 워드 클라우드 이미지를 파일로 저장
    wordcloud.to_file(image_file_name)
    print(f'Word Cloud saved as {image_file_name}')