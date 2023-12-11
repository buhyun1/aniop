<template>
  <div class="mid">
    <img class="logo" src="@/assets/mainlogo.svg" alt="logo" />
    <div class="aniop">ANIOP</div>
  </div>
</template>

<script>
export default {
  mounted() {
    // 로딩 후 3초 후에 홈 페이지로 이동
    setTimeout(() => {
      this.$router.push("/");
    }, 3000);
  },
};
</script>

<style>
.mid {
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
.logo {
  width: 90px;
  height: 90px;
  animation: spin 2s linear infinite;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.aniop {
  margin-top: 20px;
  font-size: 44px;
  font-weight: bold;
}
</style>
