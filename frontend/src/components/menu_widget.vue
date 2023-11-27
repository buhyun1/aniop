<template>
  <div class="menu-widget">
    <div class="logo-title">
      <router-link to="/">
        <img src="@/assets/aniop_logo.png" alt="logo" />
      </router-link>
      <router-link to="/" class="title">Aniop</router-link>
    </div>
    <div class="menu">
      <router-link
        to="/serviceIntroduce"
        class="menu-intro"
        @click="menuClicked('serviceIntroduce')"
        >서비스 소개</router-link
      >
      <router-link
        to="/clipingTab"
        class="menu-clip"
        @click="menuClicked('clipingTab')"
        >뉴스 클리핑</router-link
      >
    </div>
  </div>
</template>
    

<script>
export default {
  methods: {
    menuClicked(menuItem) {
      if (this.currentPageIs()) {
        // currentPageIsSSS 메소드는 현재 페이지가 sss인지 확인합니다.
        this.showConfirmDialog(() => {
          this.$router.push({ name: menuItem }); // 사용자가 확인을 클릭한 경우 해당 페이지로 이동
        });
      } else {
        this.$router.push({ name: menuItem }); // sss 페이지가 아니면 바로 이동
      }
    },
    showConfirmDialog(callback) {
      if (
        confirm(
          "확인을 누르면 정보가 사라집니다. 그래도 페이지를 이동하시겠습니까?"
        )
      ) {
        callback();
      }
    },
    currentPageIs() {
      // 현재 라우트가 'sss'인지 확인하는 로직 구현
      return this.$route.name === "/clipingTab"; // 예시로 'sss'를 라우트 이름으로 가정
    },
  },
};
</script>
    <style scoped>
.menu-widget {
  display: flex;
  align-items: center;
  margin-top: 4%;
  margin-left: 4%;
}

.logo-title {
  display: flex;
  align-items: center;
}

.menu {
  display: flex;
  margin-left: 10%;
}

.title {
  font-size: 40px;
  font-weight: bold;
  border: none;
  background-color: transparent;
  text-decoration: none;
  color: black;
}

.menu-intro,
.menu-clip {
  font-size: 24px;
  font-weight: 600;
  border: none;
  background-color: transparent;
  text-decoration: none;
  color: black;
}

@media (max-width: 1000px) {
  .logo-title {
    display: none;
  }

  .menu {
    display: none;
  }
}

@media (min-width: 1001px) {
  .logo-title {
    justify-content: space-between;
    width: 12%;
  }

  .menu {
    justify-content: space-between;
    width: 50%;
  }
}
</style>