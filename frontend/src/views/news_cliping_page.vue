<template>
  <div id="app">
    <menu-widget></menu-widget>
    <div class="period">기간</div>

    <VDatePicker id="left" v-model="date" />
    <VDatePicker id="right" v-model="date" />
    <side-bar></side-bar>
    <div>
      <button class="complete">완료</button>
      <itemwidget></itemwidget>
      <newscliping></newscliping>
    </div>
  </div>
</template>

<script>
import menu from "@/components/menu_widget.vue";
import sidebar from "@/components/sidebar_widget.vue";
import itemwidget from "@/components/item_widget.vue";
import newscliping from "@/components/newscliping_widget.vue"

export default {
  components: {
    "menu-widget": menu,
    "side-bar": sidebar,
    "itemwidget": itemwidget,
    "newscliping": newscliping
  },
};

</script>

<style>
  @media(max-width: 1001px) {
    .complete{
      display: none;
    }
  }

.complete{
  /* Button */

position: absolute;
width: 112px;
height: 49px;
bottom: 25%;
right: 15%;

background: #0070FF;
/* Shadow 3 */
box-shadow: -5px -5px 10px rgba(255, 255, 255, 0.5), 5px 5px 10px rgba(170, 170, 204, 0.25), 10px 10px 20px rgba(170, 170, 204, 0.5), -10px -10px 20px #FFFFFF;
border-radius: 32px;
font-weight: bold;
font-size: 15px;
color: #FFFFFF;
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

.period{
  font-weight: bold;
  font-size: 30px;
  color: #0070FF;
  position: absolute;
  top: 30%;
  left: 30%;
}

 @media(max-width: 1001px) {
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

  @media(max-width: 700px) {
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