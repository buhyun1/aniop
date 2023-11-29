from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
import json

def extract_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # JSON 데이터 로드
        text = ''
        for article in data:
            if 'Body' in article and article['Body']:
                text += article['Body']
        return text

# 텍스트에서 불용어 제거 및 워드 클라우드 생성
def generate_wordcloud(text, stopwords=None):
    # 불용어 설정 (예시)
    default_stopwords = set(['이', '그', '저', '수', '것', '등', '있', '하', '것이다', '이다', '에서', '으로', '에는', '의', '에', '을', '를', '이', '가', '으로', '에서', '에는', '의'])
    if stopwords:
        default_stopwords = default_stopwords.union(stopwords)

    # 단어 분리 및 빈도 계산
    words = re.findall(r'\w+', text)
    filtered_words = [word for word in words if word not in default_stopwords]
    word_counts = Counter(filtered_words)

    # 워드 클라우드 생성
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

    return wordcloud

import json  # JSON 모듈 추가

# JSON 파일에서 데이터 로드
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 데이터 추출
text = extract_text('data.json')

# 워드 클라우드 생성 및 시각화
wordcloud = generate_wordcloud(text)

# 워드 클라우드 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
