# 백엔드 Dockerfile
# Node 이미지를 베이스로 사용
FROM node:lts
# 작업 디렉토리 설정
WORKDIR ./backend
# 의존성 파일들 복사
COPY ./package*.json ./
# npm을 이용하여 의존성 설치
RUN npm install

# 나머지 소스 코드 복사
COPY . .
# 백엔드 서버가 사용할 포트 설정
EXPOSE 3000
# 백엔드 서버 실행
CMD [ "node", "src/server.js" ]
