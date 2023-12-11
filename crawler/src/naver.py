import requests
from bs4 import BeautifulSoup

section_urls ={
"shipbuilding":"https://search.naver.com/search.naver?where=news&sm=tab_jum&query=스마트조선+ESG+경영", #스마트 조선
"construction":"https://search.naver.com/search.naver?where=news&sm=tab_jum&query=스마트건설+ESG+경영", #스마트 건설
"ittech":'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=it동향', #it 동향
"safety":"https://search.naver.com/search.naver?where=news&sm=tab_jum&query=안전", #안전
"industrialaccident":"https://search.naver.com/search.naver?where=news&sm=tab_jum&query=산업재해", #산업재해
"seriousdisaster":"https://search.naver.com/search.naver?where=news&sm=tab_jum&query=중대재해처벌법" #중대재해
}
import requests
from bs4 import BeautifulSoup

# 페이지 번호와 키워드별 URL 정의
page = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]
section_urls = {
"shipbuilding": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=스마트조선+ESG+경영&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=52&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start=",
"construction": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%8A%A4%EB%A7%88%ED%8A%B8%EA%B1%B4%EC%84%A4%20ESG%20%EA%B2%BD%EC%98%81&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=20&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start=",
"ittech": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=it동향&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=52&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start=",
"safety": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=안전&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=52&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start=",
"industrialaccident": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=산업재해&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=52&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start=",
"seriousdisaster": "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=중대재해처벌법&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=52&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:all,a:all&start="
}

# 각 키워드별 뉴스 제목을 저장할 딕셔너리
news_titles = {keyword: [] for keyword in section_urls}

# 각 페이지와 키워드별 URL을 순회하면서 뉴스 제목 추출
for i in page:
    for keyword, base_url in section_urls.items():
        url = f"{base_url}{i}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url} (status code: {response.status_code})")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # 뉴스 제목 선택 및 추출
        news_links = soup.select('a.news_tit')
        page_titles = [link.get('title') for link in news_links]
        news_titles[keyword].extend(page_titles)

# 결과 출력
for keyword, titles in news_titles.items():
    print(f"{keyword}: {titles}")  # 각 키워드별 첫 10개의 제목 출력
