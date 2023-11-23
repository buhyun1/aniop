<template>
  <div class="text-container">
    <p>뉴스 클리핑</p>
    <div class="highlight-text"><p>목록 확인</p></div>
    <p>미리 보기</p>
  </div>
</template>
  
  <script>
export default {};
</script>
  
  <style scoped>
.text-container {
  display: flex;
  flex-direction: column;
  margin-top: 160px;
  margin-left: 140px;
  position: fixed;
  z-index: 2;
}

.text-container p {
  margin-bottom: 40px;
  font-size: 28px;
}

.highlight-text p {
  font-size: 36px;
  color: #0070FF;
}

@media (max-width: 1001px) {
  .text-container {
    display: none;
  }
}
</style>
  