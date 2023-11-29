<template>
  <div>
    <div class="tabs-container">
      <div class="tab-content">
        <div class="tab-content-box">
          <div class="scrollable-content">
            <div class="news-content">
              <h3>산업정책</h3>
              <div>
                <div v-for="item in policyItems" :key="item.ArticleID">
                  <a :href="item.ArticleLink" target="_blank">{{
                    item.Title
                  }}</a>
                </div>
              </div>
            </div>
            <div class="news-content">
              <h3>건설/조선 디지털화</h3>
              <div>
                <div v-for="item in digitalItems" :key="item.ArticleID">
                  <a :href="item.ArticleLink" target="_blank">{{
                    item.Title
                  }}</a>
                </div>
              </div>
            </div>
            <div class="news-content">
              <h3>IT</h3>
              <div>
                <div v-for="item in itItems" :key="item.ArticleID">
                  <a :href="item.ArticleLink" target="_blank">{{
                    item.Title
                  }}</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <button class="copy" @click="selectScrollableContent">복사</button>

      <button class="complete" @click="redirectToLoading">완료</button>
    </div>
  </div>
</template>
  
<script>
export default {
  props: {
    previewdata: Array,
  },
  data() {
    return {
      isLoading: true,
    };
  },

  methods: {
    selectScrollableContent() {
      const content = this.$el.querySelector(".scrollable-content");
      let range;
      if (document.body.createTextRange) {
        // 대부분의 IE 브라우저에서
        range = document.body.createTextRange();
        range.moveToElementText(content);
        range.select();
      } else if (window.getSelection) {
        // 대부분의 비-IE 브라우저에서
        const selection = window.getSelection();
        range = document.createRange();
        range.selectNodeContents(content);
        selection.removeAllRanges();
        selection.addRange(range);
      }

      try {
        document.execCommand("copy"); // 선택된 텍스트를 클립보드에 복사
        alert("복사되었습니다!"); // 성공 알림
      } catch (err) {
        console.error("복사 실패:", err);
      }
    },
    formatContent(content) {
      return content.replace(/\n/g, "<br>");
    },
    redirectToLoading() {
      this.$router.push("/loading");
    },
  },
  computed: {
    policyItems() {
      return this.previewdata.filter((item) => item.CategoryID === 0);
    },
    digitalItems() {
      return this.previewdata.filter(
        (item) => item.CategoryID === 1 || item.CategoryID === 2
      );
    },
    itItems() {
      return this.previewdata.filter((item) => item.CategoryID === 3);
    },
  },
};
</script>
  
<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
.copy {
  position: absolute;
  width: 100px;
  height: 50px;
  bottom: 20%;
  right: 28.5%;
  background-color: #0070ff;
  border: none;
  opacity: 0.7;
  border-radius: 32px;
  font-weight: bold;
  font-size: 15px;
  color: #ffffff;
}
.complete {
  position: absolute;
  width: 100px;
  height: 50px;
  bottom: 20%;
  right: 22%;
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
  height: 75vh;
  width: 1100px;
}

.tabs {
  display: flex;
  margin-bottom: 10px;
  color: #0070ff;
}

.tab {
  cursor: pointer;
  font-size: 20px;
}

.active-tab {
  font-size: 24px;
}

.tab-content > div {
  margin-right: 30%;
  width: 900px;
}

.tab-content > div.show {
  display: block;
}
</style>
