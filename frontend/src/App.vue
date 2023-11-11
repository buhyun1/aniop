<template>
  <div id="app">
    <menu-widget></menu-widget>
    <sidebar-widget></sidebar-widget>
  </div>
</template>

<script>
import MenuWidget from "./components/menu_widget.vue";
import SidebarWidget from "./components/sidebar_widget.vue";

export default {
  components: {
    "menu-widget": MenuWidget,
    "sidebar-widget": SidebarWidget,
  },
};
</script>

<style>
.centered-text {
  text-align: center;
  margin: 150px;
margin-left: 500px;
}

.centered-text p {
  margin-bottom: 30px;
}
</style>