import torch
from transformers import BertConfig, BertTokenizer, BertForSequenceClassification
import json
from mymodel import MyModel1
import boto3
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv('../../.env')

# 환경 변수 가져오기
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')

def load_model(model_path, number_of_labels, tokenizer_path='bert-base-uncased'):
    config = BertConfig.from_pretrained(tokenizer_path, num_labels=number_of_labels)
    model = MyModel1(config) # 설정 파일 로드

    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
    tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
    model.eval()  # 평가 모드로 설정
    return model, tokenizer

def predict(model, tokenizer, input_text):
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    return probabilities.numpy()

def lambda_handler(event, context):
    s3 = boto3.client('s3', 
                      region_name=region_name, 
                  aws_access_key_id=aws_access_key_id, 
                  aws_secret_access_key=aws_secret_access_key)

    # S3 버킷과 파일 이름
    bucket = event['bucket']
    input_file_key = event['input_file']
    output_file = event['output_file']

    # S3에서 입력 파일 읽기
    input_obj = s3.get_object(Bucket=bucket, Key=input_file_key)
    input_data = json.loads(input_obj['Body'].read().decode('utf-8'))

    #model, tokenizer = load_model('./model.pth', 4)
    model, tokenizer = load_model('../models/kobert/model.pth', 4)

   # 출력 데이터 준비
    outdata = input_data.copy()
    
    for article in outdata['news']:
        input_text = article['Title']  # 'Title' 키 사용
        prediction = predict(model, tokenizer, input_text)
        predicted_category = prediction.argmax(axis=1).item()
        article['Category'] = predicted_category

    # 결과를 JSON 문자열로 변환
    output_json = json.dumps(outdata, ensure_ascii=False)

    # S3에 결과 파일 쓰기
    s3.put_object(Body=output_json, Bucket=bucket, Key=output_file)

    return {
        'statusCode': 200,
        'body': json.dumps('File uploaded successfully')
    }


# 로컬 테스트
if __name__ == "__main__":
    test_event = {'bucket': 'aniop2023', 
                  'input_file': '20231122_combined_news.json', 
                  'output_file': '20231122_combined_news_2.json'}
    test_context = None
    result = lambda_handler(test_event, test_context)
    print(result)