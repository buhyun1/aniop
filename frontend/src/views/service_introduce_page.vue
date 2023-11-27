<template>
<div>
  <menuWidget />
  <div class="centered-container">
    <div class="introbox">
      <div class="introtitle">서비스 소개</div>
      <div class="introtext">
        <p>
          이 프로젝트는 "Musma's Pick"이라는 뉴스레터 섹션을 자동으로 생성하는
          시스템을 구축하는 것입니다.
        </p>
        <p>
          신뢰할 수 있는 출처에서 뉴스 기사를 크롤링 해오고, 콘텐츠 분석을
          수행하며, 콘텐츠 생성을 위해
        </p>
        <p>
          Chat GPT를 사용합니다. 또한 뉴스레터 콘텐츠에 대한 필터링 및 예약
          옵션도 제공합니다.
        </p>
      </div>
      <hr class="line" style="border: 1px color= #0070ff" width="1000px" />
      <img class="intro_person" src="@/assets/intro_person.svg" />
    </div>
  </div>
</div>
</template>

<script>
import menuWidget from "@/components/menu_widget.vue";

export default {
  components: {
    menuWidget,
  },
};
</script>

  <style>
.centered-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 140px;
}

.introbox {
  margin-top: 20px;
}
.introtext p {
  margin-bottom: 20px;
}
.line {
  position: absolute;
  bottom: 10%;
  left: 20%;
}

.introtitle {
  font-size: 40px;
  font-weight: bold;
  text-align: left;
  width: 930px;
}

.introtext {
  font-size: 20px;
  width: 930px;
  margin-top: 95px;
}
.intro_person {
  position: absolute;
  right: 20%;
  bottom: 15%;
  width: 250px;
  height: 250px;
}
@media (max-width: 1200px) {
  .intro_person {
    display: none;
  }
}
@media (max-width: 1001px) {
  .intro_person,
  .line {
    display: none;
  }
  .introtext,
  .introbox {
    width: 400px;
    height: 400px;
  }
  .introtitle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 400px;
  }
}
</style>