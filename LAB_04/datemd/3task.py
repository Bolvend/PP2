from datetime import datetime, timedelta

date_str = input("Write date in YYYY-MM-DD HH:MM:SS.MS format: ")               

dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")

formatted = dt_obj.strftime("%Y-%m-%d %H:%M:%S") 
print(formatted)
