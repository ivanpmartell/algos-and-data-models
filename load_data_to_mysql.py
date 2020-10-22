import sys
import calendar
import mysql.connector as mysqldb
from mysql.connector import ProgrammingError

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
    _, date_time_month, date_time_day, date_time_time, _, date_time_year = values[3].split(' ')
    string_values = f"{values[0]},{int(values[1],16)},{date_time_year}-{abbr_to_num[date_time_month]}-{date_time_day} {date_time_time},{values[4]}"
    return string_values

def get_columns_Checkins():
    cols = "userId,venueId,utcTime,utcOffset"
    return cols

def post_insert_Venues():
    #ALTER TABLE Venues ADD FOREIGN KEY (assignedCity) REFERENCES Cities(id);
    return """ALTER TABLE Venues ADD CONSTRAINT fk_country FOREIGN KEY (countryCode) REFERENCES Countries(code);
            ALTER TABLE Venues ADD SPATIAL INDEX(latlon);"""

def post_insert_Checkins():
    return "ALTER TABLE Checkins ADD FOREIGN KEY (venueId) REFERENCES Venues(id);"


table_name = sys.argv[1]
file_path = files[table_name]
out_file = "data/{table_name}.csv"
cursor = mysqldb_connection.cursor()
create_table_query = f"CREATE TABLE {table_name} (" + ','.join(create_columns[table_name]) + ");"
try:
    cursor.execute(create_table_query)
except ProgrammingError as e:
    print("Warning: " + e.msg)
cursor.close()
print("Creating file...")
with open(out_file, 'a') as out_file:
    with open(file_path, 'r') as read_file:
        for i, line in enumerate(read_file):
            if i > 99999:
                break
            values = line.rstrip().split('\t')
            out_file.write(locals()[f"insert_{table_name}"](values) +"\n")

query = f"LOAD DATA INFILE {out_file} INTO TABLE {table_name} " +\
"""FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'"""
print("Running query...")
cursor = mysqldb_connection.cursor()
cursor.execute(query)
mysqldb_connection.commit()
cursor.close()
cursor = mysqldb_connection.cursor()
cursor.execute(locals()[f"post_insert_{table_name}"]())
cursor.close()