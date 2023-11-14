import pandas as pd

# 파일 로드
file_path = './data/processed/manual_crawling_news_titles .xlsx'
news_df = pd.read_excel(file_path)

# 'safety', 'industrialaccident', 'seriousdisaster' 열을 하나로 합치기
news_df['industrial_policy_trends'] = news_df['safety'].astype(str) + ' ' + \
                                      news_df['industrialaccident'].astype(str) + ' ' + \
                                      news_df['seriousdisaster'].astype(str)

# 불필요한 열 제거
news_df = news_df.drop(columns=['safety', 'industrialaccident', 'seriousdisaster'])

# Excel 파일로 저장
saved_file_path = './data/processed/processed_crawling_news_titles.xlsx'
news_df.to_excel(saved_file_path, index=False)