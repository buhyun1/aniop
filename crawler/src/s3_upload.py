import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import re
import time
from concurrent.futures import ThreadPoolExecutor
import json 
import boto3
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()


def get_news_titles(section_url, reg_date):
    all_titles = []
    page = 1
    prev_items = None  # Store the previous page's items

    while True:
        url = f"{section_url}{page}&regDate={reg_date}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to retrieve {section_url} (Status Code: {response.status_code})")
            break

        print(f"Processing {section_url} {page}")
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.select('.box_etc li > div.cont_thumb > strong.tit_thumb')

        # Check if current page items are the same as the previous page
        if prev_items == news_items:
            print(f"No new articles found for {section_url} page {page}. Ending the process.")
            break

        if not news_items:
            print(f"No more articles found for {section_url} page {page}. Moving to next section.")
            break

        for item in news_items:
            title = item.select_one('a.link_txt').text.strip()
            link = item.select_one('a.link_txt')['href']
            all_titles.append({"Title": title, "Link": link})

        prev_items = news_items  # Update previous items
        page += 1
        
    return all_titles

# Define a function to check if an article is in English
def is_english(text):
    words = text.split()
    english_words = [word for word in words if re.match(r'^[a-zA-Z]+$', word)]
    return len(english_words) / len(words) > 0.5 if words else False

# Define a function to extract article content
def extract_article_content(url):
    print(f"Extracting content from {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_paragraphs = soup.select("div.article_view section p")
        article_text = '\n'.join([para.text for para in article_paragraphs])
        return article_text.strip()
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return ""
async def crawler():
    logging.debug("Starting the crawler function")

    # Define section URLs
    section_urls = {
        #"digital": "https://news.daum.net/breakingnews/digital?page=",
        "society_affair":"https://news.daum.net/breakingnews/society/affair?page=",
        # "society_others":"https://news.daum.net/breakingnews/society/others?page=",
        # "society_labor":"https://news.daum.net/breakingnews/society/labor?page=",
        # "society_environment":"https://news.daum.net/breakingnews/society/environment?page=",
        # "politics_administration":"https://news.daum.net/breakingnews/politics/administration?page=",
        # "politics_assembly":"https://news.daum.net/breakingnews/politics/assembly?page=",
        # "politics_others":"https://news.daum.net/breakingnews/politics/others?page=",
        # "politics_dipdefen":"https://news.daum.net/breakingnews/politics/dipdefen?page=",
        # "politics_president":"https://news.daum.net/breakingnews/politics/president?page=",
        # "economic_industry":"https://news.daum.net/breakingnews/economic/industry?page=",
        # "economic_others":"https://news.daum.net/breakingnews/economic/others?page=",
        # "economic_world":"https://news.daum.net/breakingnews/economic/world?page="
    }

    # Get today's date
    today = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

    # Record start time
    start_time = time.time()

    # Create a list to store dataframes for each section
    dataframes = []

    # Iterate through section URLs and crawl news
    for section_name, section_url in section_urls.items():
        news_titles = get_news_titles(section_url, today)

        # Convert to DataFrame
        news_df = pd.DataFrame(news_titles)

        # Add filtering criteria here
        news_df = news_df[~news_df['Title'].str.contains('\\[포토\\]|\\[인사\\]|\\[부고\\]|\\[사진\\]|\\[동영상\\]')]
        news_df = news_df[~news_df['Title'].apply(is_english)]

        # Extract article content (you can uncomment this if needed)
        # with ThreadPoolExecutor(max_workers=10) as executor:
        #     news_df['Article'] = list(executor.map(extract_article_content, news_df['Link']))

        # Filter out short or empty articles (you can uncomment this if needed)
        # news_df = news_df[news_df['Article'].str.len() > 50]
        # news_df = news_df[news_df['Article'].str.strip() != '']

        # Save to Excel
        excel_filename = f'{today}_{section_name}_news.xlsx'
        #news_df.to_excel(excel_filename, index=False, engine='openpyxl')
        print(f"Successfully saved {section_name} news to {excel_filename}")
        # Append the DataFrame to the list
        dataframes.append(news_df)
    # Concatenate DataFrames from different sections
    combined_df = pd.concat(dataframes)
    # 데이터프레임을 딕셔너리로 변환
    data = {
        "news": []
    }
    for index, row in combined_df.iterrows():
        news_item = {
            "Title": row['Title'],
            "Link": row['Link']
        }
        data["news"].append(news_item)
    #for docker
    #json_filename = f'src/data/{today}_combined_news.json'

    #for local
    json_filename = f'./data/{today}_combined_news.json'
    try:
        # JSON 파일 저장
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
        print(f"Successfully saved combined news to {json_filename}")
    except Exception as e:
        print(f"Error saving combined news to {q}: {e}")

    # Record end time and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time elapsed for crawling: {elapsed_time} seconds")

    # 환경 변수에서 액세스 키와 시크릿 키 추출
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # S3 클라이언트 생성, 인증 정보 포함
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # 업로드할 파일 이름과 버킷 이름 설정
    file_name = json_filename
    bucket_name = 'aniop2023'

    # 파일을 S3에 업로드
    try:
        s3.upload_file(file_name, bucket_name, os.path.basename(file_name))
        # 다운로드 성공 메시지 출력
        print("S3 파일 업로드 완료")
        logging.info(f"Uploaded {file_name} to S3 bucket {bucket_name} as {file_name[9:]}")
        return file_name[9:]
        #models 컨테이너에 get 요청
    except Exception as e:
        # 다운로드 실패 메시지 출력
        print(f"S3 파일 업로드 오류: {str(e)}")