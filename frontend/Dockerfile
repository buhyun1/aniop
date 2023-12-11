# 프론트엔드 Dockerfile
# Node 이미지를 베이스로 사용
FROM node:lts as frontend-server-stage
# 작업 디렉토리 설정
WORKDIR /frontend
# 소스 코드 복사
COPY . .
# 개발 서버 실행 (npm run serve)
CMD ["npm", "run", "serve"]
