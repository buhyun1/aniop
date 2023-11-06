# aniop
2023 소프트웨어공학 뉴스클리핑 깃허브 작업 공간입니다. 

# 작업 내용
GitHub Commit Message Guide
커밋 메시지는 코드 변경사항을 명확하게 전달하는 것이 중요합니다. 아래의 가이드를 따라 효과적인 커밋 메시지를 작성해보세요.

Commit Message Format
<타입>(<범위>): <제목> <본문> <꼬리말>

### 타입
커밋의 유형을 나타냅니다.

feat: 새로운 기능 추가

fix: 버그 수정

docs: 문서 변경

style: 코드 스타일 변경 (포맷팅 등, 코드 변경 없음)

refactor: 코드 리팩토링

test: 테스트 코드 추가 및 변경 (비즈니스 로직에 변경 없음)

chore: 빌드 스크립트 설정, 라이브러리 업데이트 등 기타 변경

### 범위
변경사항의 범위를 간략하게 표기 (예: auth, api, ui).

### 제목
커밋의 요약. 50자 이내로 작성합니다.

### 본문
커밋의 세부 내용. 필요한 경우에만 사용합니다.

### 예시
new : components/MyPageImage.vue<br>
feat : MyPageView.vue에서 라우터 연결<br> 
chore : HomeView.vue에서 배경화면 색 변경<br> 
docs : README 수정<br>
refactor : LogIn.vue 코드 여백 정리<br> 