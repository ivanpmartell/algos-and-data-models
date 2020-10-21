import mysql.connector as mysqldb
from mysql.connector import ProgrammingError

mysqldb_connection = mysqldb.connect(host='localhost', user='ivan', password='CSC501@ssignments', database='assignment1')

files = {"Countries": "data/dataset_TIST2015_Countries.txt", #This file was created by the bash script
         "Cities": "data/dataset_TIST2015_Cities.txt"}

create_columns = {"Countries": ["code CHAR(2) NOT NULL",
                                "name VARCHAR(25) NOT NULL",
                                "PRIMARY KEY (code)"],
                  "Cities": ["id SMALLINT UNSIGNED AUTO_INCREMENT",
                             "name VARCHAR(30) NOT NULL",
                             "latlon POINT NOT NULL",
                             "countryCode CHAR(2) NOT NULL",
                             "isNationalCapital BOOLEAN DEFAULT FALSE",
                             "isProvincialCapital BOOLEAN DEFAULT FALSE",
                             "isEnclave BOOLEAN DEFAULT FALSE",
                             "PRIMARY KEY (id)",
                             "FOREIGN KEY (countryCode) REFERENCES Countries(code)",
                             "SPATIAL INDEX(latlon)"]}

# Selected spatial point as data for lat lon because the indices make use of r-trees 

def insert_Countries(values):
    insert_query = f"INSERT INTO Countries (code,name) VALUES(" + "'{0}'".format("','".join(values)) + ");"
    return insert_query

def insert_Cities(values):
    valid_name = values[0].replace("\'", "\'\'")
    string_values = f"'{valid_name}',POINT({values[1]},{values[2]}),'{values[3]}'"
    cols = "name,latlon,countryCode"
    if values[-1] != 'Other':
        "isNationalCapital", "isProvincialCapital", "isEnclave"
        if values[-1] == 'National and provincial capital':
            cols += ",isNationalCapital,isProvincialCapital"
            string_values += ",TRUE,TRUE"
        elif values[-1] == 'National capital':
            cols += ",isNationalCapital"
            string_values += ",TRUE"
        elif values[-1] == 'National capital and provincial capital enclave':
            cols += ",isNationalCapital,isProvincialCapital,isEnclave"
            string_values += ",TRUE,TRUE,TRUE"
        elif values[-1] == 'Provincial capital':
            cols += ",isProvincialCapital"
            string_values += ",TRUE"
        elif values[-1] == 'Provincial capital enclave':
            cols += ",isProvincialCapital,isEnclave"
            string_values += ",TRUE,TRUE"
    insert_query = f"INSERT INTO Cities (" + cols + ") VALUES(" + string_values + ");"
    return insert_query


for table_name, file_path in files.items():
    cursor = mysqldb_connection.cursor()
    create_table_query = f"CREATE TABLE {table_name} (" + ','.join(create_columns[table_name]) + ");"
    try:
        cursor.execute(create_table_query)
    except ProgrammingError as e:
        print("Warning: " + e.msg)
    cursor.close()
    with open(file_path, 'r') as read_file:
        for line in read_file:
            values = line.rstrip().split('\t')
            cursor = mysqldb_connection.cursor()
            insert_query = locals()[f"insert_{table_name}"](values)
            cursor.execute(insert_query)
            cursor.close()
        mysqldb_connection.commit()