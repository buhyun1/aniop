<template>
  <div>
    <menuWidget />
    <div class="tabs-container">
      <div class="tabs">
        <ul>
          <li
            v-for="(tab, index) in tabs"
            :key="index"
            @click="changeTab(index)"
            :class="{ active: activeTab === index }"
          >
            {{ tab.name }}
          </li>
        </ul>
      </div>

      <div class="content">
        <div class="tab-content">
          <component
            :is="currentTabComponent"
            :newsData="newsData"
            @dataReceived="handleDataReceived"
            @clickReceived="handleclickReceived"
          />
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
import menuWidget from "@/components/menu_widget.vue";
import newsCliping from "@/views/news_cliping_page.vue";
import checkList from "@/views/check_list_page.vue";
import preview from "@/views/preview_page.vue";

export default {
  components: {
    menuWidget,
  },
  data() {
    return {
      newsData: null,

      tabs: [
        { name: "뉴스 클리핑", component: newsCliping },
        { name: "목록 확인", component: checkList },
        { name: "미리 보기", component: preview },
      ],
      activeTab: 0,
      responseData: null,
      currentTabComponent: "newsCliping",
    };
  },
  mounted() {
    this.changeTab(this.activeTab);
  },
  methods: {
    changeTab(index) {
      this.activeTab = index;
      this.currentTabComponent = this.tabs[index].component;
    },
    handleDataReceived(data) {
      this.newsData = data;
      this.changeTabToCheckList(); // 목록 확인 탭으로 전환
    },
    changeTabToCheckList() {
      const checkListIndex = this.tabs.findIndex(
        (tab) => tab.name === "목록 확인"
      );
      if (checkListIndex !== -1) {
        this.currentTabComponent = this.tabs[checkListIndex].component;
        this.activeTab = checkListIndex; // 활성 탭 인덱스 업데이트
      }
    },
    handleclickReceived() {
      this.changeTabTopreview(); // 목록 확인 탭으로 전환
    },
    changeTabTopreview() {
      const checkListIndex = this.tabs.findIndex(
        (tab) => tab.name === "미리 보기"
      );
      if (checkListIndex !== -1) {
        this.currentTabComponent = this.tabs[checkListIndex].component;
        this.activeTab = checkListIndex; // 활성 탭 인덱스 업데이트
      }
    },
  },
};
</script>
  
  <style scoped>
.tabs-container {
  display: flex;
  justify-content: center; /* 수평 가운데 정렬을 추가합니다. */
}
.tabs {
  flex: 1;
  margin-top: 10%;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  text-align: center;
  padding: 10px;
  cursor: pointer;
  margin-bottom: 50px;
  font-size: 28px;
}

li.active {
  color: #0070ff;
  font-size: 36px;
}

.content {
  flex: 3;
  z-index: 2;
}

/* .sidebar {
  border-top-right-radius: 30px;
  position: fixed;
  bottom: 0;
  left: 0;
  background: rgba(217, 217, 217, 0.2);
  z-index: 0;
} */

@media (min-width: 1000px) {
  .sidebar {
    width: 340px;
    height: 76vh;
  }
}

@media (max-width: 1001px) {
  .sidebar {
    display: none;
  }
  .tabs {
    display: none;
  }
}
</style>
  