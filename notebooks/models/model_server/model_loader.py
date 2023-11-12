from sentence_transformers import SentenceTransformer
import logging
import time
import torch
# 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


model = None

def load_model():
    global model
    logger.info("모델 로드 시작")
    model_path = '../kpf-sbert'  # 모델 경로
    start_time = time.time()
    model = SentenceTransformer(model_path)
    end_time = time.time()
    logger.info(f"모델 로드 완료: {model_path}")
    logger.info(f"로딩 시간: {end_time - start_time:.2f}초")


def get_model():
    global model
    if torch.cuda.is_available():
        device = torch.device("cuda")
        model.to(device)
        print("GPU 사용 가능: 모델을 CUDA로 이동")
    else:
        device = torch.device("cpu")
        print("GPU 사용 불가능: CPU에서 모델 실행")
    if model is None:
        load_model()
    torch.save(model.state_dict(), 'model.pt')

    return model

def __main__():
    get_model()

