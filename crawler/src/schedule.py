import logging
import requests
import datetime

# 로깅 설정
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='/home/ubuntu/cron_log.txt', level=logging.DEBUG, format=log_format)

try:
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 현재 날짜와 시간 가져오기
    logging.debug(f"Start request at {current_time}")  # 시작 시간 로그에 기록

    # API 호출 로직
    response = requests.get("http://localhost:8080/crawling")

    # API 응답 처리
    if response.status_code == 200:
        logging.info(f"API 호출 성공 - 상태 코드: {response.status_code}")
        # 원하는 작업 수행
        pass
    else:
        # API 호출이 실패한 경우 예외 발생
        raise Exception(f"API 호출 실패 - 상태 코드: {response.status_code}")

except Exception as e:
    # 예외 처리 및 로그 기록
    logging.error(f"에러 발생: {str(e)}")
