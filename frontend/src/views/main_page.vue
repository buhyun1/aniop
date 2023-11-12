<template>
  <div class="center">
  <div class="first">
      2023-2 부경대학교
      <br>기술데이터공학전공 소프트웨어공학
  </div>
  <div class="second">
      ANIOP<br>(All News In One Page)
  </div>
      <div class="image-container">
          <img class="image" src="@/assets/people.svg">
          <img class="image" src="@/assets/워드클라우드.jpeg">
      </div>
  </div>
</template>

<style>
.center{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.first{
  text-align: center;
  font-weight: bold;
}
@media(min-width: 1000px) {
  .first {
      font-size: 24px;
  }
}

@media(max-width: 1001px) {
  .first {
      font-size: 24px;
  }

  .center{
      display: flex;
      flex-flow: column; 
      position: absolute;
      justify-content: center;
      align-items: center;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0; 
  }
}

.second{
  text-align: center;
  color: #0070FF;
  font-weight: bold;
  margin: 20px;
}
@media(min-width: 1000px) {
  .second {
      font-size: 24px;
  }

  .image {
      width: 340px;
      height: 340px;
  } 
}

@media(max-width: 1001px) {
  .second {
      font-size: 34px;
  }

  .image {
      display: none;
  }
}


</style>