import torch
from transformers import BertConfig, BertTokenizer, BertForSequenceClassification
import json
from mymodel import MyModel1

def load_model(model_path, number_of_labels, tokenizer_path='bert-base-uncased'):
    config = BertConfig.from_pretrained(tokenizer_path, num_labels=number_of_labels)
    model = MyModel1(config) # 설정 파일 로드
    model.load_state_dict(torch.load(model_path))
    tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
    model.eval()  # 평가 모드로 설정
    return model, tokenizer

def predict(model, tokenizer, input_text):
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    return probabilities.numpy()

def lambda_handler(event):
    number_of_labels = 4
    model_path = './model.pth'
    model, tokenizer = load_model(model_path, number_of_labels)
    
    # 입력 데이터 처리
    with open(event, 'r') as file:
        data = json.load(file)
    
    # 출력 데이터 준비
    outdata = data.copy()
    
    for article in outdata['news']:
        input_text = article['title']
        prediction = predict(model, tokenizer, input_text)
        # 카테고리 예측 결과 추가 (예시: 가장 높은 확률을 가진 카테고리 인덱스)
        predicted_category = prediction.argmax(axis=1).item()
        article['category'] = predicted_category

    return outdata

# 파일 경로
predict_file_path = './predicted_data.json'

# 함수 실행
result = lambda_handler(predict_file_path)

# 결과 출력
print(result)