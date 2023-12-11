import os
from dotenv import load_dotenv
import openai

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 및 기타 설정 가져오기
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = os.getenv('OPENAI_API_version')

# 환경 변수 확인
print(f"OPENAI_API_TYPE: {openai.api_type}")
print(f"OPENAI_API_KEY: {openai.api_key}")
print(f"OPENAI_API_BASE: {openai.api_base}")
print(f"OPENAI_API_VERSION: {openai.api_version}")

response = openai.ChatCompletion.create(
    engine="teamlab-gpt-35-turbo",
    messages=[
    {
      "role": "user",
      "content": "Answer the question What's for lunch today with a noun?"
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response['choices'][0]['message']['content'])
