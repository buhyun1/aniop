<script>
import TestModel from '@/models/testModel.vue';
export default {
  data() {
    return {
      newsItems: []
    };
  },
  async created() {
    try {
      // headers 변수를 선언하고 초기화합니다.
      const headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json',
        // 기타 필요한 헤더들을 추가하세요.
      };
      const modelInstance = new TestModel();
      this.newsItems = await modelInstance.fetchData(headers);
    } catch (error) {
      console.error('데이터를 불러오는 중 에러가 발생했습니다:', error);
    }
  }
};
</script>