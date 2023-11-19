<template>
  <menuWidget />
  <div class="center">
    <div class="first">
      2023-2 부경대학교
      <br />기술데이터공학전공 소프트웨어공학
    </div>
    <div class="second">ANIOP<br />(All News In One Page)</div>
    <div class="image-container">
      <img class="image" src="@/assets/people.svg" />
    </div>
  </div>
</template>

<script>
import menuWidget from "@/components/menu_widget.vue";

export default {
  components: {
    menuWidget
  },
};
</script>

<style>
.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 100px;
}

.first {
  text-align: center;
  font-weight: bold;
}
@media (min-width: 1000px) {
  .first {
    font-size: 36px;
  }
}

@media (max-width: 1001px) {
  .first {
    font-size: 36px;
  }

  .center {
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

.second {
  text-align: center;
  color: #0070ff;
  font-weight: bold;
  margin: 20px;
}
@media (min-width: 1000px) {
  .second {
    font-size: 28px;
  }

  .image {
    margin-top: 5px;
    width: 480px;
    height: 480px;
  }
}

@media (max-width: 1001px) {
  .second {
    font-size: 36px;
  }

  .image {
    margin-top: 5px;
    width: 480px;
    height: 480px;
  }
}
</style>
