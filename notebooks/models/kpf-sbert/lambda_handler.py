import json
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
from sklearn.cluster import AgglomerativeClustering
import hdbscan
import logging


# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def load_model(model_path):
    model = SentenceTransformer(model_path)
    return model

# Function to process UMAP
def umap_process(corpus_embeddings, n_components=5):
    return umap.UMAP(n_neighbors=15, n_components=n_components, metric='cosine').fit_transform(corpus_embeddings)

def cluster_texts(model, input_texts):
    embeddings = model.encode(input_texts)
    reduced_embeddings = umap_process(embeddings, n_components=5)

    # Agglomerative Clustering
    agg_cluster = AgglomerativeClustering(n_clusters=None, distance_threshold=0.3)
    agg_labels = agg_cluster.fit_predict(reduced_embeddings)

    # HDBSCAN Clustering
    hdbscan_cluster = hdbscan.HDBSCAN(min_cluster_size=3, gen_min_span_tree=True)
    hdbscan_labels = hdbscan_cluster.fit_predict(reduced_embeddings)

    return agg_labels, hdbscan_labels

def lambda_handler(event):
    logger.info("Extracting titles and categories from the event.")
    model_path = './model_file'  # Adjust the path as needed
    model = load_model(model_path)

  # Extract titles from the event
    logger.info("Extracting titles and categories from the event.")
    articles = event['articles']
    titles = [article['title'] for article in articles]
    categories = [article['category'] for article in articles]
    
     # Perform clustering
    logger.info("Performing clustering on the extracted titles.")
    agg_labels, hdbscan_labels = cluster_texts(model, titles)
    
    # Assign clusters to the data
    logger.info("Assigning clusters to the data.")

    clustered_data = []
    for i, title, category in zip(range(len(titles)), titles, categories):
        clustered_data.append({
            'title': title,
            'category': category,
            'Agglomerative_Cluster': agg_labels[i],
            'HDBSCAN_Cluster': hdbscan_labels[i]
        })
    logger.info("Clustering completed. Returning results.")
    return clustered_data
# Example event data
event = {
  "articles": [
    {
      "title": "삼성전자, 새로운 5G 칩셋 출시 예정",
      "category": "기술"
    },
    {
      "title": "한국 정부, 재생 가능 에너지에 대한 투자 증가",
      "category": "환경"
    },
    {
      "title": "국내 코로나19 백신 개발, 임상시험 단계 진입",
      "category": "보건"
    },
    {
      "title": "한류 열풍, 전 세계적으로 K-팝의 인기 상승 중",
      "category": "문화"
    },
    {
      "title": "한국 경제 성장률, 올해 상반기 중 예측치 초과 달성",
      "category": "경제"
    },
    {
      "title": "국내 최고 기업들의 채용 공고 증가, 일자리 시장 활성화 기대",
      "category": "경영"
    },
    {
      "title": "서울시, 대중교통 체계 개편안 발표",
      "category": "정책"
    },
    {
      "title": "한국 영화 '기생충', 국제 영화제에서 다수 상 수상",
      "category": "엔터테인먼트"
    },
    {
      "title": "인공지능을 활용한 농업 기술, 농가 수익성 향상에 기여",
      "category": "농업"
    },
    {
      "title": "국내 대학들, 온라인 교육 플랫폼 확대 계획 발표",
      "category": "교육"
    }
  ]
}

# Execute the function
result = lambda_handler(event)

# Print the results
print(result)