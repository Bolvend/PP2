from datetime import datetime, timedelta

date_str = input("Write date in YYYY-MM-DD format: ")
date = datetime.strptime(date_str, "%Y-%m-%d")

five_days = timedelta(days=5)

new_datetime = date - five_days

print("Дата 5 дней назад:", new_datetime.strftime("%Y-%m-%d"))
