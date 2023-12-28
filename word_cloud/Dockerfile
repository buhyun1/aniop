# 베이스 이미지로 python 3.9을 사용
# Python 베이스 이미지 사용
FROM python:3.8-slim-buster

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends tzdata g++ git curl
# RUN apt-get update && apt-get instal -y openjdk-8-jdk openjdk-8-jre
# ENV LANG=C.UTF-8
# ENV JAVA_HOME /usr/lib/jvm/java-1.8-openjdk/jre
# RUN pip install --upgrade pip
# RUN pip install JPype1
# RUN pip install konlpy

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 Python 라이브러리 목록을 포함하는 requirements.txt 파일 복사
COPY requirements.txt .


# Python 라이브러리 설치

RUN pip install -r requirements.txt

# 현재 디렉토리의 모든 파일을 작업 디렉토리로 복사
COPY . .

# Flask 서버 실행을 위한 포트 번호 지정
EXPOSE 5000

# Java 환경 변수 설정
# ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
# ENV PATH $PATH:$JAVA_HOME/bin

# Flask 애플리케이션 실행 명령어
CMD ["python", "word_cloud_generator.py"]
