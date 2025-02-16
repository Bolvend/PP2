from datetime import datetime, timedelta

date_str = input("Write date in YYYY-MM-DD HH:MM:SS format: ")               

dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

formatted = datetime.now() - dt_obj

skok_prozhil = timedelta.total_seconds(formatted)

print(skok_prozhil)

