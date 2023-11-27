<template>
  <div id="app">
    <div class="period">기간</div>

    <VDatePicker id="left" v-model="date" />
    <VDatePicker id="right" v-model="date" />
    <div>
      <button class="complete">완료</button>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
@media (max-width: 1001px) {
  .complete {
    display: none;
  }
}

.complete {
  position: absolute;
  width: 100px;
  height: 50px;
  bottom: 20%;
  right: 10%;
  background-color: #0070ff;
  border: none;
  opacity: 0.7;
  border-radius: 32px;
  font-weight: bold;
  font-size: 15px;
  color: #ffffff;
}

#left {
  position: absolute;
  left: 40%;
  top: 30%; /* 추가된 속성 */
}

#right {
  position: absolute;
  left: 65%;
  top: 30%; /* 추가된 속성 */
}

.period {
  font-weight: bold;
  font-size: 24px;
  color: #0070ff;
  position: absolute;
  top: 30%;
  left: 30%;
}

@media (max-width: 1001px) {
  #left {
    position: absolute;
    left: 10%;
    top: 30%;
  }
  .period {
    position: absolute;
    top: 10%;
    left: 40%;
  }
  #right {
    position: absolute;
    left: 50%;
    top: 30%;
  }
}

@media (max-width: 700px) {
  #left {
    display: none;
  }
  .period {
    position: absolute;
    top: 50%;
    left: 50%;
  }
  #right {
    display: none;
  }
}
</style>