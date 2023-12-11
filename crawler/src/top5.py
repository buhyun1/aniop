import mysql.connector
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import re
import openai
import datetime
# .env 파일 로드 및 환경 변수 로드
load_dotenv()
host = os.getenv('MYSQL_HOST')
port = int(os.getenv('MYSQL_PORT'))
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')

# 환경 변수에서 API 키 및 기타 설정 가져오기
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = os.getenv('OPENAI_API_version')

# 환경 변수 확인
print(f"OPENAI_API_TYPE: {openai.api_type}")
print(f"OPENAI_API_KEY: {openai.api_key}")
print(f"OPENAI_API_BASE: {openai.api_base}")
print(f"OPENAI_API_VERSION: {openai.api_version}")

def summarize_news(news_body):
    if len(news_body) >4000:
        words=news_body[:2000]+news_body[-2000:]
        news_body=words
    response = openai.ChatCompletion.create(
    engine="teamlab-gpt-35-turbo",
    messages=[
    {
      "role": "user",
      "content": f"Summarize a given article in 100 characters in Korean:  {news_body}"
    }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    res = response['choices'][0]['message']['content']
    print(res)
    return res



def select_top5():
    #전날 날짜 계산
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    # 데이터베이스 연결 설정
    conn = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
    cursor = conn.cursor()
    print("데이터베이스 연결 성공")

    # 카테고리 0부터 4까지 반복
    for category_id in range(5):
        #query = "SELECT ArticleLink FROM Articles WHERE CategoryID = %s ORDER BY DailyRelatedArticleCount DESC LIMIT 5"
        query = """
        SELECT ArticleLink FROM Articles 
        WHERE CategoryID = %s AND ArticleLink Like %s 
        ORDER BY DailyRelatedArticleCount DESC LIMIT 5
        """
        Date="%"+yesterday+"%"
        cursor.execute(query, (category_id,Date))
        print(f"Category ID {category_id}: 쿼리 실행 완료")

        for (link,) in cursor.fetchall():
            try:
                print(f"기사 링크 처리 중: {link}")
                response = requests.get(link)
                print(f"웹 요청 상태 코드: {response.status_code}")
                soup = BeautifulSoup(response.text, 'html.parser')
                article_paragraphs = soup.select("div.article_view section p")
                article_text = '\n'.join([para.text for para in article_paragraphs])
                content = article_text.strip()
                print("기사 내용 추출 완료")

                # URL에서 날짜 추출
                match = re.search(r'\d{8}', link)
                date = match.group() if match else None
                print(f"날짜 추출: {date}")
                # 뉴스 요약
                summary = summarize_news(content) if content else None
                print(f"기사 요약 완료: {summary}")

                # 본문, 날짜 및 요약 내용을 데이터베이스에 업데이트
                if content and date and summary:
                    update_query = "UPDATE Articles SET Body = %s, PublishedDate = %s, Summary = %s WHERE ArticleLink = %s"
                    cursor.execute(update_query, (content, date, summary, link))
                    print('SQL 업데이트 완료')

            except Exception as e:
                print(f"오류 발생: {e}")             
    # 변경 사항을 데이터베이스에 커밋
    conn.commit()
    # print("데이터베이스 커밋 완료")
    # delete_query = """
    # DELETE FROM Articles 
    # WHERE (PublishedDate IS NULL) 
    # AND (Summary IS NULL OR Summary = '')
    # """
    # cursor.execute(delete_query)
    # print("오래된 또는 업데이트되지 않은 기사 삭제 완료")
    # conn.commit()
    # print("삭제 커밋완료")
    # 연결 종료
    cursor.close()
    conn.close()
    print("데이터베이스 연결 종료")
    
if __name__ == "__main__":
    select_top5()