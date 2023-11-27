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
    <div class="tab-content">
      <div v-show="currentTab === 0" class="tab-content-box">
        <div class="news-content">
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 무스마, Oiltech
            그룹과 인도시장 OSS 서비스 제공을 위한 각서 체결
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 무스마, Oiltech
            그룹과 인도시장 OSS 서비스 제공을 위한 각서 체결
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 무스마, Oiltech
            그룹과 인도시장 OSS 서비스 제공을 위한 각서 체결
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 무스마, Oiltech
            그룹과 인도시장 OSS 서비스 제공을 위한 각서 체결
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 무스마, Oiltech
            그룹과 인도시장 OSS 서비스 제공을 위한 각서 체결
          </h3>
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

      <div v-show="currentTab === 1" class="tab-content-box">
        <div class="news-content">
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 조선업계 기술
            전략의 변화.. 디지털전환과 디지털트윈
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 조선업계 기술
            전략의 변화.. 디지털전환과 디지털트윈
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 조선업계 기술
            전략의 변화.. 디지털전환과 디지털트윈
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 조선업계 기술
            전략의 변화.. 디지털전환과 디지털트윈
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 조선업계 기술
            전략의 변화.. 디지털전환과 디지털트윈
          </h3>
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

      <div v-show="currentTab === 2" class="tab-content-box">
        <div class="news-content">
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 애플의 실수와
            실패의 역사, 그냥 버리기엔 너무 아까운 실패들
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 애플의 실수와
            실패의 역사, 그냥 버리기엔 너무 아까운 실패들
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 애플의 실수와
            실패의 역사, 그냥 버리기엔 너무 아까운 실패들
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 애플의 실수와
            실패의 역사, 그냥 버리기엔 너무 아까운 실패들
          </h3>
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
          <h3>
            <input type="checkbox" id="agreementCheckbox" /> 애플의 실수와
            실패의 역사, 그냥 버리기엔 너무 아까운 실패들
          </h3>
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
    <div><button class="complete">완료</button></div>
  </div>
</template>
  
  <script>
export default {
  data() {
    return {
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
  },
};
</script>
  
  <style scoped>
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
  