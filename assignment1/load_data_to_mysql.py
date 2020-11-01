import os
import sys
import calendar
import mysql.connector as mysqldb
from mysql.connector import ProgrammingError
from datetime import datetime, timedelta

mysqldb_connection = mysqldb.connect(host='localhost', user='ivan', password='CSC501@ssignments', database='assignment1')

abbr_to_num = {abbr: num for num, abbr in enumerate(calendar.month_abbr) if num}

files = {"Venues": "data/dataset_TIST2015_POIs.txt",
         "Checkins": "data/dataset_TIST2015_Checkins.txt"}

create_columns = {
            "Venues": ["id BINARY(96)", #int('hexId', 16)
                       "latlon POINT NOT NULL",
                       "category VARCHAR(50) NOT NULL",
                       "countryCode CHAR(2) NOT NULL",
                       "assignedCity SMALLINT UNSIGNED",
                       "PRIMARY KEY (id)"],
            "Checkins": ["id INT UNSIGNED NOT NULL AUTO_INCREMENT",
                        "userId MEDIUMINT UNSIGNED NOT NULL",
                        "venueId BINARY(96) NOT NULL",
                        "utcTime DATETIME NOT NULL",
                        "utcOffset SMALLINT NOT NULL",
                        "localDatetime DATETIME NOT NULL",
                        "PRIMARY KEY (id)"]}

# Selected spatial point as data for lat lon because the indices make use of r-trees 
# Using INT(4), which amounts to 4 bytes=32 bits, as largest id will be 33,278,683 which uses 25 bits

def insert_Venues(values):
    valid_category = values[3].replace("\'", "\'\'")
    string_values = f"{int(values[0],16)},POINT({values[1]},{values[2]}),\"{valid_category}\",\"{values[4]}\""
    return string_values

def get_columns_Venues():
    cols = "id,latlon,category,countryCode"
    return cols

def insert_Checkins(values):
    _, date_time_month, date_time_day, date_time_time, _, date_time_year = values[2].split(' ')
    date_time_string = f"{date_time_year}-{str(abbr_to_num[date_time_month]).zfill(2)}-{date_time_day} {date_time_time}"
    date_time_hour, date_time_minutes, date_time_seconds = date_time_time.split(':')
    d = datetime(year=int(date_time_year), month=abbr_to_num[date_time_month], day=int(date_time_day), hour=int(date_time_hour), minute=int(date_time_minutes), second=int(date_time_seconds))
    d_offset = timedelta(minutes=int(values[3]))
    local_time = d + d_offset
    string_values = f"{values[0]},{int(values[1],16)},{date_time_string},{values[3]},{str(local_time)}"
    return string_values

def get_columns_Checkins():
    cols = "userId,venueId,utcTime,utcOffset,localDatetime"
    return cols

def post_insert_Venues():
    #ALTER TABLE Venues ADD FOREIGN KEY (assignedCity) REFERENCES Cities(id);
    return ["ALTER TABLE Venues ADD CONSTRAINT fk_country FOREIGN KEY (countryCode) REFERENCES Countries(code);",
            "ALTER TABLE Venues ADD SPATIAL INDEX(latlon);"]

def post_insert_Checkins():
    return ["ALTER TABLE Checkins ADD FOREIGN KEY (venueId) REFERENCES Venues(id);"]


table_name = sys.argv[1]
file_path = files[table_name]
out_path = f"data/{table_name}.csv"
cursor = mysqldb_connection.cursor()
create_table_query = f"CREATE TABLE {table_name} (" + ','.join(create_columns[table_name]) + ");"
try:
    cursor.execute(create_table_query)
except ProgrammingError as e:
    print("Warning: " + e.msg)
cursor.close()
print("Creating file...")
""" with open(out_path, 'a') as out_file:
    with open(file_path, 'r') as read_file:
        for i, line in enumerate(read_file):
            values = line.rstrip().split('\t')
            try:
                out_file.write(locals()[f"insert_{table_name}"](values) +"\n")
            except:
                print(f"Error in line {i}: {line}") """

cursor = mysqldb_connection.cursor()
cursor.execute("show variables like 'secure_file_priv';")
mysql_file_path = cursor.fetchone()[1]
cursor.close()
print(f"Please move the created file '{out_path}' to {mysql_file_path}")
print(f"Command: sudo cp {out_path} {mysql_file_path}{table_name}.csv")
input("Press enter to continue...")

columns = locals()[f"get_columns_{table_name}"]()
query = f"LOAD DATA INFILE '{mysql_file_path}{table_name}.csv' INTO TABLE {table_name} " +\
r"""FIELDS TERMINATED BY ',' ENCLOSED BY '"'""" + f"LINES TERMINATED BY '\\n' ({columns})"

cursor = mysqldb_connection.cursor()
cursor.execute(query)
mysqldb_connection.commit()
cursor.close()
cursor = mysqldb_connection.cursor()
for post_query in locals()[f"post_insert_{table_name}"]():
    print("Running query: %s" % post_query)
    cursor.execute(post_query)
cursor.close()