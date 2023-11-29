<template>
  <div id="app">
    <div class="period">기간</div>

    <VDatePicker id="left" v-model="startDate" />
    <VDatePicker id="right" v-model="endDate" />
    <div>
      <button class="complete" @click="postData">완료</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { format } from "date-fns";

export default {
  data() {
    return {
      startDate: null,
      endDate: null,
      responseData: [],
    };
  },
  methods: {
    postData() {
      if (new Date(this.startDate) > new Date(this.endDate)) {
        alert("시작 날짜는 종료 날짜보다 이전이어야 합니다.");
        return;
      }
      const formattedStartDate = this.startDate
        ? format(this.startDate, "yyyy-MM-dd")
        : null;
      const formattedEndDate = this.endDate
        ? format(this.endDate, "yyyy-MM-dd")
        : null;
      const requestData = {
        startdate: formattedStartDate,
        enddate: formattedEndDate,
      };

      axios
        .post("http://localhost:3000/api/articles/by-date", requestData)
        .then((response) => {
          console.log("데이터 전송 성공:", response.data);
          this.$emit("dataReceived", response.data);

          /*this.$emit("dataReceived", response.data);
          this.$emit("changeTab", "목록 확인");*/
        })
        .catch((error) => {
          console.error("데이터 전송 중 오류 발생:", error);
        });
    },
  },
};
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
  right: 18%;
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