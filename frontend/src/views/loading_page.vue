<template>
  <div class="mid">
    <img class="logo" src="@/assets/mainlogo.svg" alt="logo" />
    <div class="aniop">ANIOP</div>
  </div>
</template>

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
}
.aniop {
  margin-top: 20px;
  font-size: 44px;
  font-weight: bold;
}
</style>