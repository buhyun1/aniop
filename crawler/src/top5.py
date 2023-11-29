import mysql.connector
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import re
from openai import OpenAI


# .env 파일 로드 및 환경 변수 로드
load_dotenv()
host = os.getenv('MYSQL_HOST')
port = int(os.getenv('MYSQL_PORT'))
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')

def summarize_news(news_body):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=os.getenv('api_key'),
    )

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Summarize a given article in 100 characters in Korean: {news_body}",
            }
        ],
        model="gpt-3.5-turbo",
    )
    # 요약 추출
    # 올바른 응답 데이터 추출 방법
    if completion is not None and completion.choices:
        result_text = completion.choices[0].message.content
    return result_text

# 데이터베이스 연결 설정
conn = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
cursor = conn.cursor()

# 카테고리 0부터 4까지 반복
for category_id in range(5):
    query = query = """
    SELECT ArticleLink FROM Articles 
    WHERE CategoryID = %s AND (Summary IS NULL OR Summary = '') 
    ORDER BY DailyRelatedArticleCount DESC LIMIT 5
    """
    cursor.execute(query, (category_id,))

    for (link,) in cursor.fetchall():
        try:
            print(f"기사 링크 처리 중: {link}")
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            article_paragraphs = soup.select("div.article_view section p")
            article_text = '\n'.join([para.text for para in article_paragraphs])
            content = article_text.strip()

            # URL에서 날짜 추출
            match = re.search(r'\d{8}', link)
            date = match.group() if match else None

            # 뉴스 요약
            summary = summarize_news(content) if content else None
            print(f"기사 요약 완료: {summary}")

            # 본문, 날짜 및 요약 내용을 데이터베이스에 업데이트
            if content and date and summary:
                update_query = "UPDATE Articles SET Body = %s, PublishedDate = %s, Summary = %s WHERE ArticleLink = %s"
                cursor.execute(update_query, (content, date, summary, link))
                print('SQL 업데이트 완료')

            # 변경 사항을 데이터베이스에 커밋
            conn.commit()
            print("데이터베이스 커밋 1 완료")

            
            
        except Exception as e:
            print(f"오류 발생: {e}")

delete_query = "DELETE FROM Articles WHERE Body IS NULL OR Body = ''"
cursor.execute(delete_query)
conn.commit()
print("데이터베이스 커밋 2 완료")

desc_query ="SELECT * FROM Articles ORDER BY DailyRelatedArticleCount DESC;"
cursor.execute(desc_query)
conn.commit()

# 연결 종료
cursor.close()
conn.close()
print("데이터베이스 연결 종료")
