<script>
import axios from 'axios';
export default class TestModel {
  async fetchData(headers) {
    try {
      const response = await axios.get('http://15.164.165.194:3000/api/articles', { headers });
      return response.data;
    } catch (error) {
      console.error(error);
      return [];
    }
  }
}
</script>