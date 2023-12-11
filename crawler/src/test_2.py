import datetime
#전날 날짜 계산
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
print("yesterday", type(yesterday))