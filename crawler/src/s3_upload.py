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
        #"society_affair":"https://news.daum.net/breakingnews/society/affair?page=",
        #"society_others":"https://news.daum.net/breakingnews/society/others?page=",
        #"society_labor":"https://news.daum.net/breakingnews/society/labor?page=",
        #"society_environment":"https://news.daum.net/breakingnews/society/environment?page=",
        #  "politics_administration":"https://news.daum.net/breakingnews/politics/administration?page=",
        #  "politics_assembly":"https://news.daum.net/breakingnews/politics/assembly?page=",
        #  "politics_others":"https://news.daum.net/breakingnews/politics/others?page=",
        #  "politics_dipdefen":"https://news.daum.net/breakingnews/politics/dipdefen?page=",
        #  "politics_president":"https://news.daum.net/breakingnews/politics/president?page=",
        "economic_industry":"https://news.daum.net/breakingnews/economic/industry?page=",
        #  "economic_others":"https://news.daum.net/breakingnews/economic/others?page=",
        #"economic_world":"https://news.daum.net/breakingnews/economic/world?page="
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
       
        word_list = [
        "산업정책", "경제정책", "제조업", "기술 혁신", "수출규제", "무역정책", "지역산업", "그린 에너지", "디지털화", "자동화",
        "고용정책", "국내 생산", "외국 진출", "연구 개발", "스타트업 지원", "금융 지원", "자원 개발", "정부 지원금", "산업 클러스터", "블록체인",
        "인공지능", "사물인터넷", "빅데이터", "로봇 공학", "3D 프린팅", "클린 에너지", "태양광 발전", "전기차", "바이오 기술", "생명 공학",
        "의료 기술", "헬스케어", "항공우주 산업", "자동차 산업", "반도체 산업", "통신 기술", "5G", "기술", "사이버 보안", "로봇산업", "디지털 거래",
        "무인 자동차", "스마트 시티", "스마트 그리드", "4차 산업혁명", "지능형 제조", "융합 기술", "국제 무역", "글로벌 공급망", "자원 절약", "환경 보호",
        "지속 가능성", "혁신 생태계", "경제 성장", "녹색 산업", "자동차 배터리", "생산성 향상", "투자 환경", "소비자 보호", "정부 정책", "산업 협회",
        "연방 정부", "지방 정부", "규제 개혁", "시장 개방", "무역 협정", "해외 진출", "기술 이전", "연구 협력", "고용 창출", "미래 노동",
        "혁신 지원", "특허 정책", "지식재산권", "산업 규모", "유통 산업", "소매업", "서비스 산업", "문화 산업", "교육 산업", "농업 정책",
        "어업 정책", "광업 정책", "에너지 정책", "화학 산업", "강철 산업", "석유 산업", "건설 산업", "부동산 시장", "금융 서비스", "보험 업계",
        "미래 도시", "스마트 물류", "로봇 기술", "인재 양성", "국제 경쟁력", "정책 평가", "경제 예측", "산업 통계", "지식 경제", "디지털 정부"
        "디지털 건설", "조선 산업", "인공지능", "AI", "스마트 건축", "해양 기술", "머신 러닝",
        "건설 기술", "조선 디지털화", "딥 러닝", "빌딩 정보 모델링", "BIM", "스마트 조선", "자연어 처리", "NLP",
        "디지털 트윈", "조선 디지털 혁신", "빅데이터", "가상 건축", "클라우드 컴퓨팅",
        "현장 자동화", "조선 로봇화", "IoT", "사물인터넷", "자동화 기술", "블록체인",
        "건설 로봇", "조선 제조 프로세스", "가상현실", "VR", "스마트 도시", "빅데이터 조선", "증강현실", "AR",
        "3D 프린팅 건설", "인공지능 조선", "사이버 보안", "디지털 건설 플랫폼", "3D 인쇄 조선", "데이터 분석",
        "클라우드 기술", "스마트 조선장비", "로봇 공학", "건설 소프트웨어", "조선 IoT", "자율 주행 자동차",
        "건설 데이터 분석", "해양 로봇", "5G 네트워크", "무인 항공기", "드론", "조선 블록체인", "산업 4.0",
        "건설 로봇 공학", "조선 디지털 플랫폼", "디지털 트랜스포메이션", "디지털 건설 경영", "조선 소프트웨어",
        "모바일 앱 개발", "가상 현장 투어", "조선 데이터 분석", "컴퓨터 비전", "디지털 품질 관리",
        "해양 드론", "인터넷 보안", "건설 프로젝트 관리 소프트웨어", "조선 로봇 공학", "머신 비전",
        "디지털 마케팅", "스마트 건물 시스템", "디지털 조선 경영", "가상 개발 환경", "건설 로봇화",
        "가상 조선", "머신러닝 알고리즘", "현장 센서", "조선 디지털 트랜스포메이션", "자율 주행 로봇",
        "블록체인 기술", "조선 디지털 시스템", "데이터 사이언스", "스마트 건설 장비", "클라우드 컴퓨팅",
        "소프트웨어 개발", "건설 자동화 솔루션", "조선 자동화 솔루션", "사물인터넷 플랫폼", "로봇 건설 작업",
        "해양 로봇 기술", "빅데이터 분석 도구", "미래 건설 기술", "조선 로봇 작업", "블록체인 기술",
        "건설 디지털 트랜스포메이션", "미래 조선 기술", "클라우드 보안", "건설 혁신", "조선 디지털 품질 관리",
        "디지털 미디어", "스마트 건설 재료", "스마트 조선 시스템", "사물인터넷 보안", "디지털 토탈 스테이션", "DTS",
        "조선 로봇화 공정", "디지털 경제", "무선 센서 네트워크", "조선 디지털 플랫폼 통합", "디지털 정부",
        "건설 IoT 플랫폼", "조선 IoT 센서", "정보 보안", "건설 로보틱스", "조선 로봇 인프라",
        "소셜 미디어", "AI 기반 건설", "블록체인 기술", "디지털 헬스케어", "스마트 도로 건설",
        "조선 스마트 장비", "디지털 교육", "로봇 건설 장비", "디지털 조선 품질 보증", "로봇 프로세스 자동화",
        "건설 데이터 분석 도구", "조선 로봇 AI", "머신 러닝 프레임워크", "건설 현장 로봇", "스마트 조선 자동화",
        "가상화 기술","산업정책", "경제정책", "제조업", "기술혁신", "수출규제", "무역정책", "지역산업", "그린에너지", "디지털화", "자동화",
        "고용정책", "국내생산", "외국진출", "연구개발", "스타트업지원", "금융지원", "자원개발", "정부지원금", "산업클러스터", "블록체인",
        "인공지능", "사물인터넷", "빅데이터", "로봇공학", "3D프린팅", "클린에너지", "태양광발전", "전기차", "바이오기술", "생명공학",
        "의료기술", "헬스케어", "항공우주산업", "자동차산업", "반도체산업", "통신기술", "5G", "기술", "사이버보안", "로봇산업", "디지털거래",
        "무인자동차", "스마트시티", "스마트그리드", "4차산업혁명", "지능형제조", "융합기술", "국제무역", "글로벌공급망", "자원절약", "환경보호",
        "지속가능성", "혁신생태계", "경제성장", "녹색산업", "자동차배터리", "생산성향상", "투자환경", "소비자보호", "정부정책", "산업협회",
        "연방정부", "지방정부", "규제개혁", "시장개방", "무역협정", "해외진출", "기술이전", "연구협력", "고용창출", "미래노동",
        "혁신지원", "특허정책", "지식재산권", "산업규모", "유통산업", "소매업", "서비스산업", "문화산업", "교육산업", "농업정책",
        "어업정책", "광업정책", "에너지정책", "화학산업", "강철산업", "석유산업", "건설산업", "부동산시장", "금융서비스", "보험업계",
        "미래도시", "스마트물류", "로봇기술", "인재양성", "국제경쟁력", "정책평가", "경제예측", "산업통계", "지식경제", "디지털정부",
        "디지털건설", "조선산업", "인공지능", "AI", "스마트건축", "해양기술", "머신러닝",
        "건설기술", "조선디지털화", "딥러닝", "빌딩정보모델링", "BIM", "스마트조선", "자연어처리", "NLP",
        "디지털트윈", "조선디지털혁신", "빅데이터", "가상건축", "클라우드컴퓨팅",
        "현장자동화", "조선로봇화", "IoT", "사물인터넷", "자동화기술", "블록체인",
        "건설로봇", "조선제조프로세스", "가상현실", "VR", "스마트도시", "빅데이터조선", "증강현실", "AR",
        "3D프린팅건설", "인공지능조선", "사이버보안", "디지털건설플랫폼", "3D인쇄조선", "데이터분석",
        "클라우드기술", "스마트조선장비", "로봇공학", "건설소프트웨어", "조선IoT", "자율주행자동차",
        "건설데이터분석", "해양로봇", "5G네트워크", "무인항공기", "드론", "조선블록체인", "산업4.0",
        "건설로봇공학", "조선디지털플랫폼", "디지털트랜스포메이션", "디지털건설경영", "조선소프트웨어",
        "모바일앱개발", "가상개발환경", "건설로봇화",
        "가상조선", "머신러닝알고리즘", "현장센서", "조선디지털트랜스포메이션", "자율주행로봇",
        "블록체인기술", "조선디지털시스템", "데이터사이언스", "스마트건설장비", "클라우드컴퓨팅",
        "소프트웨어개발", "건설자동화솔루션", "조선자동화솔루션", "사물인터넷플랫폼", "로봇건설작업",
        "해양로봇기술", "빅데이터분석도구", "미래건설기술", "조선로봇작업", "블록체인기술",
        "건설디지털트랜스포메이션", "미래조선기술", "클라우드보안", "건설혁신", "조선디지털품질관리",
        "디지털미디어", "스마트건설재료", "스마트조선시스템", "사물인터넷보안", "디지털토탈스테이션", "DTS",
        "조선로봇화공정", "디지털경제", "무선센서네트워크", "조선디지털플랫폼통합", "디지털정부",
        "건설IoT플랫폼", "조선IoT센서", "정보보안", "건설로보틱스", "조선로봇인프라",
        "소셜미디어", "AI기반건설", "블록체인기술", "디지털헬스케어", "스마트도로건설",
        "조선스마트장비", "디지털교육", "로봇건설장비", "디지털조선품질보증", "로봇프로세스자동화",
        "건설데이터분석도구", "조선로봇AI", "머신러닝프레임워크", "건설현장로봇", "스마트조선자동화",
        "가상화기술"]
        # news_df = news_df[news_df['Title'].str.contains('\\[?\\]|\\[인사\\]|\\[부고\\]|\\[사진\\]|\\[동영상\\]')]
        filtered_df = pd.DataFrame(columns=["Title", "Link"])
        for word in word_list:
        #     #news_df = news_df[news_df['Title'].str.contains(f'{word}')]
            filtered_df = news_df[news_df['Title'].str.contains(f'{word}')]
        #     filtered_df = pd.concat([news_df, filtered_articles])
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
        dataframes.append(filtered_df)
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
    json_filename = f'src/data/{today}_combined_news.json'

    #for local
    #json_filename = f'./data/{today}_combined_news.json'
    try:
        # JSON 파일 저장
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
        print(f"Successfully saved combined news to {json_filename}")
    except Exception as e:
        print(f"Error saving combined news to {json_filename}: {e}")

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