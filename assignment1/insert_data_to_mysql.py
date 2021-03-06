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
                        "localDatetime DATETIME NOT NULL",
                        "PRIMARY KEY (id)"]}

# Selected spatial point as data for lat lon because the indices make use of r-trees 
# Using INT(4), which amounts to 4 bytes=32 bits, as largest id will be 33,278,683 which uses 25 bits

def insert_Venues(values):
    valid_category = values[3].replace("\'", "\'\'")
    string_values = f"({int(values[0],16)},POINT({values[1]},{values[2]}),'{valid_category}','{values[4]}')"
    return string_values

def start_insert_Venues():
    cols = "id,latlon,category,countryCode"
    query = f"INSERT INTO Venues (" + cols + ") VALUES"
    return query

def post_insert_Venues():
    #ALTER TABLE Venues ADD CONSTRAINT fk_city FOREIGN KEY (assignedCity) REFERENCES Cities(id);
    return ["ALTER TABLE Venues ADD CONSTRAINT fk_country FOREIGN KEY (countryCode) REFERENCES Countries(code);",
            "ALTER TABLE Venues ADD SPATIAL INDEX(latlon);"]

def insert_Checkins(values):
    _, date_time_month, date_time_day, date_time_time, _, date_time_year = values[2].split(' ')
    date_time_string = f"{date_time_year}-{str(abbr_to_num[date_time_month]).zfill(2)}-{date_time_day} {date_time_time}"
    date_time_hour, date_time_minutes, date_time_seconds = date_time_time.split(':')
    d = datetime(year=int(date_time_year), month=abbr_to_num[date_time_month], day=int(date_time_day), hour=int(date_time_hour), minute=int(date_time_minutes), second=int(date_time_seconds))
    d_offset = timedelta(minutes=int(values[3]))
    local_time = d + d_offset
    string_values = f"{values[0]},{int(values[1],16)},{date_time_string},{values[3]}"
    return string_values

def start_insert_Checkins():
    cols = "userId,venueId,utcTime,utcOffset,localDatetime"
    query = f"INSERT INTO Checkins ({cols}) VALUES"
    return query

def post_insert_Checkins():
    return ["ALTER TABLE Checkins ADD CONSTRAINT fk_venue FOREIGN KEY (venueId) REFERENCES Venues(id);"]


table_name = sys.argv[1]
file_path = files[table_name]
cursor = mysqldb_connection.cursor()
create_table_query = f"CREATE TABLE {table_name} (" + ','.join(create_columns[table_name]) + ");"
try:
    cursor.execute(create_table_query)
except ProgrammingError as e:
    print("Warning: " + e.msg)
cursor.close()
with open(file_path, 'r') as read_file:
    insert_query = locals()[f"start_insert_{table_name}"]()
    insert_strings = []
    for line in read_file:
        values = line.rstrip().split('\t')
        insert_strings.append(locals()[f"insert_{table_name}"](values))
        if len(insert_strings) > 199999:
            cursor = mysqldb_connection.cursor()
            try:
                cursor.execute(insert_query + ','.join(insert_strings) + ";")
                #mysqldb_connection.commit()
                print(cursor.rowcount, "rows were inserted.")
            except mysqldb.DatabaseError:
                raise Exception("Too many inserts. Please lower the amount of values to be inserted.")
            except ProgrammingError as e:
                print("Error: " + e.msg + ". Rolling back...")
                mysqldb_connection.rollback()
            cursor.close()
            insert_strings = []
    if len(insert_strings) > 0:
        cursor = mysqldb_connection.cursor()
        cursor.execute(insert_query + ','.join(insert_strings) + ";")
        print(cursor.rowcount, "rows were inserted.")
        cursor.close()
    mysqldb_connection.commit()

cursor = mysqldb_connection.cursor()
for post_query in locals()[f"post_insert_{table_name}"]():
    print("Running query: %s" % post_query)
    cursor.execute(post_query)
cursor.close()