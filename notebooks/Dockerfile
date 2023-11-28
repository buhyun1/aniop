# Python 이미지 사용
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /notebooks

# 필요한 Python 라이브러리 설치
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install huggingface_hub --upgrade

# 모델과 관련된 파일들 복사
COPY . .


# 모델 서버 실행 커맨드
CMD ["python", "./model_server/check_s3.py"]