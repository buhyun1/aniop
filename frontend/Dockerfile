# 프론트엔드 Dockerfile
# Node 이미지를 베이스로 사용
FROM node:lts as build-stage
# 작업 디렉토리 설정
WORKDIR /frontend
# 의존성 파일들 복사
COPY ./package*.json ./
# npm을 이용하여 의존성 설치
RUN npm install
# 나머지 소스 코드 복사
COPY . .
# Vue 앱 빌드
RUN npm run build
# 프로덕션 스테이지
FROM nginx:stable as production-stage
# 빌드된 앱 복사
COPY --from=build-stage /frontend/dist /usr/share/nginx/html
# 80번 포트 열기
EXPOSE 80
# Nginx 서버 실행
CMD ["nginx", "-g", "daemon off;"]