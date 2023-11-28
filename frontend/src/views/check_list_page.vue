<template>
  <div class="tabs-container">
    <div class="tabs">
      <div
        v-for="(tab, index) in tabs"
        :key="index"
        @click="changeTab(index)"
        :class="{ 'active-tab': currentTab === index }"
        class="tab"
      >
        {{ tab.name }}
      </div>
    </div>
    <div v-show="currentTab === 0" class="tab-content-box">
      <ul>
        <li v-for="item in policyItems" :key="item.ArticleID" class="news-item">
          <div class="checkbox-title-container">
            <input
              type="checkbox"
              class="agreementCheckbox"
              v-model="checkedItems[0][item.ArticleID]"
              @change="logCheckedItems(item.ArticleID, 0)"
            />
            <h3 class="news-title">{{ item.Title }}</h3>
          </div>
          <p class="news-summary">{{ item.Body }}</p>
        </li>
      </ul>
    </div>
    <div v-show="currentTab === 1" class="tab-content-box">
      <ul>
        <li v-for="item in digitalItems" :key="item.Title" class="news-item">
          <div class="checkbox-title-container">
            <input
              type="checkbox"
              class="agreementCheckbox"
              v-model="checkedItems[1][item.ArticleID]"
              @change="logCheckedItems(item.ArticleID, 1)"
            />
            <h3 class="news-title">{{ item.Title }}</h3>
          </div>
          <p class="news-summary">{{ item.Body }}</p>
        </li>
      </ul>
    </div>

    <div v-show="currentTab === 2" class="tab-content-box">
      <ul>
        <li v-for="item in itItems" :key="item.Title" class="news-item">
          <div class="checkbox-title-container">
            <input
              type="checkbox"
              class="agreementCheckbox"
              v-model="checkedItems[2][item.ArticleID]"
              @change="logCheckedItems(item.ArticleID, 2)"
            />
            <h3 class="news-title">{{ item.Title }}</h3>
          </div>
          <p class="news-summary">{{ item.Body }}</p>
        </li>
      </ul>
    </div>
    <div>
      <button class="complete" @click="submitSelectedArticles">완료</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    newsData: Array,
  },
  data() {
    return {
      selectedArticleIds: [],

      checkedItems: { 0: {}, 1: {}, 2: {} },
      currentTab: 0,
      tabs: [
        {
          name: "산업 정책",
        },
        {
          name: "건설/조선 디지털화",
        },
        {
          name: "IT",
        },
      ],
    };
  },

  methods: {
    changeTab(index) {
      this.currentTab = index;
    },
    formatContent(content) {
      return content.replace(/\n/g, "<br>");
    },
    logCheckedItems(articleID, tabNumber) {
      const isChecked = this.checkedItems[tabNumber][articleID];

      if (isChecked) {
        // 체크박스가 선택되면 배열에 articleID 추가
        if (!this.selectedArticleIds.includes(articleID)) {
          this.selectedArticleIds.push(articleID);
        }
      } else {
        // 체크박스가 해제되면 배열에서 articleID 제거
        const index = this.selectedArticleIds.indexOf(articleID);
        if (index !== -1) {
          this.selectedArticleIds.splice(index, 1);
        }
      }

      console.log("Selected Article IDs:", this.selectedArticleIds);
    },
    submitSelectedArticles() {
      const postData = {
        articleIds: this.selectedArticleIds,
      };

      axios
        .post("http://localhost:3000/api/articles/by-ids", postData)
        .then((response) => {
          console.log("Response Data:", response.data);
          this.$emit("clickReceived", response.data);

          // 여기서 response.data를 사용할 수 있습니다
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
  },
  computed: {
    policyItems() {
      return this.newsData.filter((item) => item.CategoryID === 0);
    },
    digitalItems() {
      return this.newsData.filter(
        (item) => item.CategoryID === 1 || item.CategoryID === 2
      );
    },
    itItems() {
      return this.newsData.filter((item) => item.CategoryID === 3);
    },
  },
};
</script>
  
  <style scoped>
ul,
li {
  list-style-type: none; /* 리스트 항목 앞의 점을 없앱니다 */
  padding: 0; /* 필요한 경우, padding을 제거합니다 */
}
.news-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.checkbox-title-container {
  display: flex;
  align-items: center;
}

.agreementCheckbox {
  margin-right: 10px;
}

.news-title {
  margin: 0; /* h3 태그의 기본 마진 제거 */
}

.news-summary {
  margin-top: 5px;
  margin-left: 25px;
  width: 670px; /* 너비 제한 */
  white-space: normal; /* 텍스트 줄바꿈 허용 */
  overflow: hidden; /* 넘치는 내용 숨기기 */
  text-overflow: ellipsis; /* 넘치는 텍스트 처리 */
  display: -webkit-box;
  -webkit-line-clamp: 3; /* 표시할 줄의 최대 수 */
  -webkit-box-orient: vertical;
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
.tab-content-box {
  max-height: 500px;
  max-width: 700px;
  overflow-y: auto;
  white-space: nowrap; /* 추가 */
  overflow-x: auto; /* 추가 */
  padding: 10px;
}
.tabs-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh;
}

.tabs {
  display: flex;
  margin-bottom: 10px;
  color: #0070ff;
}

.tab {
  cursor: pointer;
  margin-right: 200px;
  font-size: 20px;
  white-space: nowrap; /* 줄 바꿈 방지  추가 */
}

.active-tab {
  font-size: 24px;
  font-weight: bold;
}

.tab-content > div {
  margin-right: 30%;
  width: 900px;
}

.tab-content > div.show {
  display: block;
}
</style>
  