from datetime import datetime, timedelta

today = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
print(today)