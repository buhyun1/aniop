<template>
  <div class="introbox">
    <div class="introtitle">서비스 소개</div>
    <div class="introtext">
      이 프로젝트는 "Musma's Pick"이라는 뉴스레터 섹션을 자동으로 생성하는
      시스템을 구축하는 것입니다. <br />신뢰할 수 있는 출처에서 뉴스 기사를
      크롤링 해오고, 콘텐츠 분석을 수행하며, 콘텐츠 생성을 위해 <br />Chat GPT를
      사용합니다. 또한 뉴스레터 콘텐츠에 대한 필터링 및 예약 옵션도 제공합니다.
    </div>
    <hr style="border: 1px color= silver" width="70%" />
  </div>
</template>

<style>
.introbox {
  widows: 740px;
  display: flex;
  flex-flow: column;
  position: absolute;
  justify-content: center;
  align-items: center;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 1px solid red;
}
.introtitle {
  width: 740px;
  font-size: 40px;
  font-weight: bold;
  text-align: left;
  width: 930px;
}

.introtext {
  font-size: 20px;
  width: 930px;
  margin-top: 100px;
}
</style>