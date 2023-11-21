<template>
  <menuWidget />
  <checklistwidget />
  <sidebarWidget />
  <itemWidget />
</template>

<script>
import menuWidget from "@/components/menu_widget.vue";
import sidebarWidget from "../components/sidebar_widget.vue";
import itemWidget from "../components/item_widget.vue";
import checklistwidget from "@/components/checklist_widget.vue";

export default {
  components: {
    menuWidget,
    sidebarWidget,
    itemWidget,
    checklistwidget,
  },
};
</script>