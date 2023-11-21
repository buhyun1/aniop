<template>
  <menuWidget />
  <sidebarWidget />
  <itemWidget />
  <previewwidget />
</template>

<script>
import menuWidget from "@/components/menu_widget.vue";
import sidebarWidget from '../components/sidebar_widget.vue';
import itemWidget from '../components/item_widget.vue'
import previewwidget from '../components/preview_widget.vue'

export default {
  components: {
    menuWidget,
    sidebarWidget,
    itemWidget,
    previewwidget
  },
};
</script>