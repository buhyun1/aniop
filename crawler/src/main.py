import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from langdetect import detect, DetectorFactory, lang_detect_exception
import time

# 각 섹션별 URL 설정
section_urls = {
    "digital": "https://news.daum.net/breakingnews/digital?page=",
    "society": "https://news.daum.net/breakingnews/society?page=",
    "politics": "https://news.daum.net/breakingnews/politics?page=",
    "economic": "https://news.daum.net/breakingnews/economic?page=",
    "foreign": "https://news.daum.net/breakingnews/foreign?page="
}

# 오늘 날짜 설정
today = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

# 뉴스 기사를 가져오는 함수
def get_news_titles(section_url, reg_date):
    all_titles = []
    page = 1

    while True:
        # 페이지 URL 구성
        url = f"{section_url}{page}&regDate={reg_date}"
        response = requests.get(url)
        
        # 응답 코드가 200이 아닐 경우 중단
        if response.status_code != 200:
            print(f"Failed to retrieve {section_url} (Status Code: {response.status_code})")
            break
        
        print(f"Processing {section_url} page {page}")
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.select('.box_etc li > div.cont_thumb > strong.tit_thumb')

        # 기사가 더 이상 없으면 반복 중단
        if not news_items:
            print(f"No more articles found for {section_url} page {page}. Moving to next section.")
            break
        
        # 기사 제목을 리스트에 추가
        for item in news_items:
            title = item.select_one('a.link_txt').text.strip()
            link = item.select_one('a.link_txt')['href']
            all_titles.append({"Title": title, "Link": link})
        
        # 다음 페이지로 이동
        page += 1
    
    return all_titles

# 뉴스 기사 본문 추출 함수
def extract_article_content(url):
    print(f"Extracting content from {url}")  # Add this line to print the URL being processed
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_paragraphs = soup.select("div.article_view section p")
        article_text = '\n'.join([para.text for para in article_paragraphs])
        return article_text.strip()
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return ""

# 영어 감지 함수
def is_english(text):
    try:
        return detect(text) == 'en'
    except lang_detect_exception.LangDetectException:
        return False

# 일관된 결과를 위해 랜덤 시드 고정
DetectorFactory.seed = 0

# 각 섹션별 기사 데이터를 담을 리스트
all_data = []

# Start time
start_time = time.time()

# ThreadPoolExecutor를 사용하여 모든 섹션과 페이지에서 뉴스 기사 제목과 링크를 병렬로 가져오기
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_section_title = {executor.submit(get_news_titles, url, today): section for section, url in section_urls.items()}
    for future in future_to_section_title:
        section = future_to_section_title[future]
        try:
            result = future.result()
            all_data.extend(result)
            print(f"Completed: {section}")
        except Exception as exc:
            print(f"{section} generated an exception: {exc}")

# 결과를 DataFrame으로 변환
all_data_df = pd.DataFrame(all_data)

# 본문 내용 추출
with ThreadPoolExecutor(max_workers=10) as executor:
    all_data_df['Article'] = list(executor.map(extract_article_content, all_data_df['Link']))

# 필터링: 특정 문자열 제목, 짧은 기사, 빈 기사, 영어 기사 제외
all_data_df = all_data_df[~all_data_df['Title'].str.contains('\[포토\]|\[인사\]|\[부고\]')]
all_data_df = all_data_df[all_data_df['Article'].str.len() > 50]
all_data_df = all_data_df[all_data_df['Article'].str.strip() != '']
all_data_df = all_data_df[~all_data_df['Article'].apply(is_english)]

# 최종 DataFrame을 Excel 파일로 저장
excel_filename = f"{today}_total_news_articles.xlsx"
all_data_df.to_excel(excel_filename, index=False, engine='openpyxl')

print(f"Successfully saved to {excel_filename}")

# End time and total time calculation
end_time = time.time()
total_time = end_time - start_time
print(f"Successfully saved to {excel_filename}")
print(f"Total time taken: {total_time:.2f} seconds")