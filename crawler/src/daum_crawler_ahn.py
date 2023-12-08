import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

def date_in_range(publish_date, start_date, end_date):
    """
    Check if the publish_date is within the start_date and end_date range.
    """
    try:
        # 상대적인 날짜 표현을 처리
        if "시간 전" in publish_date:
            hours_ago = int(re.search(r'(\d+)시간 전', publish_date).group(1))
            publish_date = datetime.now() - timedelta(hours=hours_ago)
        elif "일 전" in publish_date:
            days_ago = int(re.search(r'(\d+)일 전', publish_date).group(1))
            publish_date = datetime.now() - timedelta(days=days_ago)
        elif "주 전" in publish_date:
            weeks_ago = int(re.search(r'(\d+)주 전', publish_date).group(1))
            publish_date = datetime.now() - timedelta(weeks=weeks_ago)
        else:
            publish_date = datetime.strptime(publish_date, '%Y-%m-%d')
        
        return start_date <= publish_date.date() <= end_date
    except Exception:
        # 날짜 형식에 맞지 않는 경우
        pass

# 사용자가 지정한 날짜 범위 설정
start_date = datetime(2023, 12, 7).date()  # 시작 날짜
end_date = datetime(2023, 12, 8).date() # 끝 날짜
print(start_date, end_date)

section_urls = {
"shipbuilding": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=조선+ESG+선박&sort=1&photo=0&field=0&pd=0&ds=&de=&cluster_rank=52&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start=",
"construction": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EA%B1%B4%EC%84%A4%EC%82%AC%20ESG%20%EA%B1%B4%EC%84%A4%ED%9A%8C%EC%82%AC&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:all,a:all&start=",
"ittech": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=it%20%EC%9D%B4%EC%8A%88%20%ED%85%8C%ED%81%AC&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:all,a:all&start=",
"safety": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%82%B0%EC%97%85%EC%95%88%EC%A0%84%20%EC%A4%91%EB%8C%80%EC%9E%AC%ED%95%B4&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:all,a:all&start="
}

import json

news_data = {keyword: [] for keyword in section_urls}

for keyword, base_url in section_urls.items():
    page_num = 1
    while True:
        url = f"{base_url}{page_num}"
        response = requests.get(url, headers=headers)
        print(url)
        print(response.text)

        if response.status_code != 200:
            print("--접속불가--")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        news_links = soup.select('a.news_tit')
        news_dates = soup.select('span.info') # 필요한 경우 날짜 정보도 추가

        for link in news_links:
            title = link.get('title')
            link_url = link.get('href')
            body = "본문 내용"  #  # body = get_news_body(link_url)

            news_data[keyword].append({
                "Title": title,
                "Body": body,
                "ArticleLink": link_url
            })

        page_num += 10

# JSON 형식으로 변환
json_data = json.dumps(news_data, ensure_ascii=False, indent=4)
print(json_data)

# # 필요한 경우 파일로 저장
# with open("news_data.json", "w", encoding="utf-8") as file:
#     file.write(json_data)
