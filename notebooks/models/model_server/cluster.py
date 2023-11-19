import pandas as pd
from sentence_transformers import SentenceTransformer
import hdbscan
import umap.umap_ as umap
from sklearn.cluster import AgglomerativeClustering
from model_loader import get_model
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def umap_process(corpus_embeddings, n_components=5):
        umap_embeddings = umap.UMAP(n_neighbors=15, n_components=n_components, metric='cosine').fit_transform(corpus_embeddings)
        return umap_embeddings

def process_embeddings_by_batch(model, titles, batch_size=32):
    embeddings = []
    for i in range(0, len(titles), batch_size):
        batch = titles[i:i + batch_size]
        batch_embeddings = model.encode(batch, show_progress_bar=True)
        embeddings.extend(batch_embeddings)
    return embeddings


def cluster_news_titles_and_save(df, file_path):
    logger.info("클러스터링 과정 시작")

    start_time = time.time()
    model = get_model()  # 모델 사용
    logger.info(f"모델 로드 완료:")

    titles = df['Title'].tolist()
    embeddings = process_embeddings_by_batch(model, titles, batch_size=32)
    logger.info("Embeddings 생성 완료")

    reduced_embeddings = umap_process(embeddings, n_components=5)
    logger.info("UMAP 차원 축소 완료")

    agg_cluster = AgglomerativeClustering(n_clusters=None, distance_threshold=0.5)
    agg_labels = agg_cluster.fit_predict(reduced_embeddings)
    logger.info("Agglomerative 클러스터링 완료")

    hdbscan_cluster = hdbscan.HDBSCAN(min_cluster_size=10, gen_min_span_tree=True)
    hdbscan_labels = hdbscan_cluster.fit_predict(reduced_embeddings)
    logger.info("HDBSCAN 클러스터링 완료")

    df['Agglomerative_Cluster'] = agg_labels
    df['HDBSCAN_Cluster'] = hdbscan_labels
    logger.info("DataFrame에 클러스터 레이블 추가 완료")

    df.to_excel(file_path, index=False)
    logger.info(f"DataFrame Excel로 저장 완료: {file_path}")

    end_time = time.time()
    logger.info(f"클러스터링 과정 완료, 총 소요 시간: {end_time - start_time:.2f}초")

    return file_path
