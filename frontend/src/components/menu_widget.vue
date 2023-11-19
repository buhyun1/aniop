<template>
    <div class="menu-widget">
      <div class="logo-title">
        <img src="@/assets/aniop_logo.png" alt="logo" />
        <div class="title">Aniop</div>
      </div>
      <div class="menu">
        <div class="menu-item">서비스 소개</div>
        <div class="menu-item">뉴스 클리핑</div>
      </div>
    </div>
  </template>
    
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
  }
  
  .menu-item {
      font-size: 24px;
      font-weight: 600;
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