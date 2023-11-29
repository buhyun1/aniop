# Python 이미지 사용
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /notebooks

# 필요한 Python 라이브러리 설치
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install huggingface_hub --upgrade


# Install cron
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# 모델과 관련된 파일들 복사
COPY . .

# python 파일 실행
#CMD ["python", "model_server/model_server.py"]

EXPOSE 80
# fast api 실행
CMD ["uvicorn", "model_server.model_server:app", "--host", "0.0.0.0", "--port", "80"]