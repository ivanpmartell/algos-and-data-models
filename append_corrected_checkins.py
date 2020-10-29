import os
import sys
import calendar
from datetime import datetime, timedelta

#Find way to correct data to the following format "Tue Apr 03 18:00:06 +0000 2012"
corrections = ["135077\t4bc8351d0050b713e9f6b93b\tWed Mar 27 17:42:97:93\t120",
                "81508\t4dc98660d4c0abe9b6320d4f\tMon21239673244639234\t-180"]
out_path = f"data/{table_name}.csv"
abbr_to_num = {abbr: num for num, abbr in enumerate(calendar.month_abbr) if num}

def insert_Checkins(values):
    _, date_time_month, date_time_day, date_time_time, _, date_time_year = values[2].split(' ')
    date_time_string = f"{date_time_year}-{str(abbr_to_num[date_time_month]).zfill(2)}-{date_time_day} {date_time_time}"
    date_time_hour, date_time_minutes, date_time_seconds = date_time_time.split(':')
    d = datetime(year=int(date_time_year), month=abbr_to_num[date_time_month], day=int(date_time_day), hour=int(date_time_hour), minute=int(date_time_minutes), second=int(date_time_seconds))
    d_offset = timedelta(minutes=int(values[3]))
    local_time = d + d_offset
    string_values = f"{values[0]},{int(values[1],16)},{date_time_string},{values[3]},{str(local_time)}"
    return string_values

print("Creating file...")
with open(out_path, 'a') as out_file:
    for i, line in enumerate(corrections):
        values = line.rstrip().split('\t')
        try:
            out_file.write(insert_Checkins(values) +"\n")
        except:
            print(f"Error in line {i}: {line}")