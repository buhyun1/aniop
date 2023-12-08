# -*- coding: utf-8 -*-

import requests
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

# 요청 사이에 무작위 지연을 추가하는 함수
def random_delay(min_delay, max_delay):
    time.sleep(random.uniform(min_delay, max_delay))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 사용자가 지정한 날짜 범위 설정
start_date = datetime(2023, 11, 8).date()  # 시작 날짜
end_date = datetime(2023, 12, 8).date() # 끝 날짜

# 날짜를 문자열 형식으로 변환
start_date_str = start_date.strftime("%Y.%m.%d")
end_date_str = end_date.strftime("%Y.%m.%d")
print(start_date_str, end_date_str)

section_urls = {
    "shipbuilding": f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%A1%B0%EC%84%A0%20ESG%20%EC%84%A0%EB%B0%95&sort=1&photo=0&field=0&pd=3&ds={start_date_str}&de={end_date_str}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{start_date_str.replace('.','')}to{end_date_str.replace('.','')},a:all&start=",
    "construction": f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B1%B4%EC%84%A4%EC%82%AC%20ESG%20%EA%B1%B4%EC%84%A4%ED%9A%8C%EC%82%AC&sort=1&photo=0&field=0&pd=3&ds={start_date_str}&de={end_date_str}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{start_date_str.replace('.','')}to{end_date_str.replace('.','')},a:all&start=",
    "ittech": f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=it%20%EC%9D%B4%EC%8A%88%20%ED%85%8C%ED%81%AC&sort=1&photo=0&field=0&pd=3&ds={start_date_str}&de={end_date_str}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{start_date_str.replace('.','')}to{end_date_str.replace('.','')},a:all&start=",
    "safety": f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%82%B0%EC%97%85%EC%95%88%EC%A0%84%20%EC%A4%91%EB%8C%80%EC%9E%AC%ED%95%B4&sort=1&photo=0&field=0&pd=3&ds={start_date_str}&de={end_date_str}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{start_date_str.replace('.','')}to{end_date_str.replace('.','')},a:all&start="
}

# 결과 출력
for key, url in section_urls.items():
    print(f"{key}: {url}")

import json

# 카테고리 ID 매핑
category_ids = {"shipbuilding": 0, "construction": 1, "ittech": 2, "safety": 3}

news_data = []

for keyword, base_url in section_urls.items():
    page_num = 1
    category_id = category_ids[keyword]

    while True:  # 페이지 순환
        url = f"{base_url}{page_num}"
        session = requests.Session()
        response = session.get(url, headers=headers)
        random_delay(1, 5)

        if response.status_code != 200:
            print("--접속불가--")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        news_links = soup.select('a.news_tit')

        # 뉴스 링크가 없으면 반복 종료
        if not news_links:
            break

        for link in news_links:  # 뉴스 순환
            title = link.get('title')

            news_data.append({
                "Title": title,
                "CategoryID": category_id
            })

        page_num += 10  # 다음 페이지로 이동

# JSON 형식으로 변환
json_data = json.dumps(news_data, ensure_ascii=False, indent=4)
print(json_data)

# 필요한 경우 파일로 저장
with open("news_data.json", "w", encoding="utf-8") as file:
    file.write(json_data)