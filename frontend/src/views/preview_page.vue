<template>
  <div>
    <div class="tabs-container">
      <button class="download">Excel</button>
      <div class="tab-content">
        <div class="tab-content-box">
          <div class="scrollable-content">
            <div class="news-content">
              <h3>산업정책</h3>
              <ul>
                <li v-for="item in previewdata" :key="item.Title">
                  <a :href="item.ArticleLink">{{ item.Title }}</a>
                </li>
              </ul>
            </div>
            <div class="news-content">
              <h3>건설/조선 디지털화</h3>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
            </div>
            <div class="news-content">
              <h3>IT</h3>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
              <p>
                &nbsp;&nbsp;&nbsp;&nbsp;산업재해 자기규율 예방체계 구축...고용부
                법령정비추진반 가동
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <button class="copy">복사</button>
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
    formatContent(content) {
      return content.replace(/\n/g, "<br>");
    },
    redirectToLoading() {
      this.$router.push("/loading");
    },
  },
};
</script>
  
<style scoped>
ul {
  list-style-type: none; /* 리스트 항목 앞의 점을 없앱니다 */
  padding: 0; /* 필요한 경우, padding을 제거합니다 */
}
.download {
  align-self: flex-end; /* 오른쪽 정렬을 위한 스타일 */
  width: 75px;
  height: 40px;
  background-color: #0070ff;
  border: none;
  opacity: 0.7;
  border-radius: 24px;
  font-weight: bold;
  font-size: 15px;
  color: #ffffff;
}
.copy {
  position: absolute;
  width: 100px;
  height: 50px;
  bottom: 20%;
  right: 16.5%;
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
  height: 75vh;
  width: 730px;
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