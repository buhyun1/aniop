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

# # 환경 변수 확인
# print(f"OPENAI_API_TYPE: {openai.api_type}")
# print(f"OPENAI_API_KEY: {openai.api_key}")
# print(f"OPENAI_API_BASE: {openai.api_base}")
# print(f"OPENAI_API_VERSION: {openai.api_version}")

def summarize_news(news_body):
    # 긴 기사를 여러 부분으로 나누기
    chunks = [news_body[i:i+2000] for i in range(0, len(news_body), 2000)]
    summaries = []

    for chunk in chunks:
        response = openai.ChatCompletion.create(
            engine="teamlab-gpt-35-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize a given article in 100 characters in Korean: {chunk}"
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        if 'choices' in response and response['choices']:
            res = response['choices'][0]['message']['content']
            summaries.append(res)
            #print(f"기사 요약 생성 완료: {res}")
        else:
            print(f"기사 요약 생성 실패: API 응답에 'choices'가 없음")

    # 모든 요약을 합쳐서 반환
    return '\n'.join(summaries)



def select_top5():
    # 전날 날짜 계산
    # yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    # print("yester")
    # 데이터베이스 연결 설정
    conn = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
    cursor = conn.cursor()
    print("데이터베이스 연결 성공")

    for category_id in range(4):
        cluster_query = """
        SELECT DBSCAN_Cluster, COUNT(*) as ArticleCount 
        FROM Articles 
        WHERE CategoryID = %s 
        GROUP BY DBSCAN_Cluster 
        ORDER BY ArticleCount DESC 
        LIMIT 5
        """
        cursor.execute(cluster_query, (category_id,))
        top_clusters = cursor.fetchall()

        print(query)
        # query = "SELECT ArticleLink, DailyRelatedArticleCount FROM Articles WHERE CategoryID = %s ORDER BY DailyRelatedArticleCount DESC LIMIT 5"
        # cursor.execute(query, (category_id,))
        
        print(f"Category ID {category_id}: 쿼리 실행 완료")
        top_article_list=[]
        for cluster_id, _ in top_clusters:
            # 각 클러스터별 최상위 기사 선택
            top_article_query = """
            SELECT ArticleLink 
            FROM Articles 
            WHERE CategoryID = %s AND DBSCAN_Cluster = %s 
            ORDER BY DailyRelatedArticleCount DESC 
            LIMIT 1
            """
            cursor.execute(top_article_query, (category_id, cluster_id))
            top_article = cursor.fetchone()
            top_article_list.append(top_article)
        
        #for (link,ArticleCount) in cursor.fetchall():
        for (link, ArticleCount) in top_article_list: 
            try:
                # 이미 저장한 기사인지 확인
                # cursor.execute("SELECT COUNT(*) FROM Articles WHERE ArticleLink = %s", (link,))
                # if cursor.fetchone()[0] > 0:
                #     print(f"기사 링크 {link}는 이미 저장되어 있으므로 무시합니다.")
                #     continue

                print(f"기사 링크 처리 중: {link}")
                response = requests.get(link)
                print(f"웹 요청 상태 코드: {response.status_code}")
                soup = BeautifulSoup(response.text, 'html.parser')
                article_title = soup.find("title").text  # 기사 제목 추출
                article_paragraphs = soup.select("div.article_view section p")
                article_text = '\n'.join([para.text for para in article_paragraphs])
                content = article_text.strip()
                print("기사 내용 추출 완료")

                # URL에서 날짜 추출
                match = re.search(r'\d{8}', link)
                date = match.group() if match else None
                print(f"날짜 추출: {date}")
                
                # 이미 저장한 기사인지 확인 (본문, 날짜, 요약을 모두 고려)
                print("content",content[:10])
                cursor.execute("SELECT COUNT(*) FROM Articles WHERE Body = %s", (content,))
                if cursor.fetchone()[0] > 0:
                    print(f"기사 본문이 이미 저장되어 있으므로 요약을 진행하지 않습니다.")
                    continue

                # 뉴스 요약
                summary = summarize_news(content) if content else None
                print(f"기사 요약 완료: {summary}")

                # 본문, 날짜, 요약 내용을 데이터베이스에 업데이트
                if content and date and summary:
                    try:                        
                        update_query = "INSERT INTO Articles (ArticleLink, Title, Body, PublishedDate, Summary, CategoryID, DailyRelatedArticleCount) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        
                        cursor.execute(update_query, (link, article_title, content, date, summary, category_id, ArticleCount))
                        print('SQL 업데이트 완료')

                        # 검증 쿼리
                        verify_query = "SELECT COUNT(*) FROM Articles WHERE ArticleLink = %s AND Title = %s AND Body = %s AND PublishedDate = %s AND Summary = %s AND CategoryID = %s"
                        cursor.execute(verify_query, (link, article_title, content, date, summary, category_id))
                        if cursor.fetchone()[0] == 0:
                            print("데이터 삽입 검증 실패: 데이터베이스에 삽입되지 않음")
                        else:
                            print("데이터 삽입 검증 성공: 데이터베이스에 삽입됨")

                    except Exception as e:
                        print(f"데이터베이스 업데이트 중 오류 발생: {e}")

            except Exception as e:
                print(f"오류 발생: {e}")      
    # 변경 사항을 데이터베이스에 커밋
    conn.commit()
    print("데이터베이스 커밋 완료")
    delete_query = """
    DELETE FROM Articles 
    WHERE (PublishedDate IS NULL) 
    AND (Summary IS NULL OR Summary = '')
    """
    cursor.execute(delete_query)
    print("오래된 또는 업데이트되지 않은 기사 삭제 완료")
    conn.commit()
    print("삭제 커밋완료")
    cursor.close()
    conn.close()
    print("데이터베이스 연결 종료")
if __name__ == "__main__":
    select_top5()