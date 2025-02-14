from datetime import datetime, timedelta

date_str = input("Write date in YYYY-MM-DD format: ")               

date = datetime.strptime(date_str, "%Y-%m-%d")
one_day = timedelta(days=1)
yesterday = date - one_day
tommorow = date + one_day

print("Yesterday:", yesterday.strftime("%Y-%m-%d"))
print("Today:", date.strftime("%Y-%m-%d"))
print("Tommorow:", tommorow.strftime("%Y-%m-%d"))