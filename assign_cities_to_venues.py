import mysql.connector as mysqldb
import collections

mysqldb_connection = mysqldb.connect(host='localhost', user='ivan', password='CSC501@ssignments', database='assignment1')

test_query = """CREATE PROCEDURE TestCities()
BEGIN
DECLARE citiesAmount INT;
DECLARE i INT;
DECLARE currentCityId INT;
DECLARE currentCityLatlon POINT;
SELECT COUNT(id) FROM Cities INTO citiesAmount;
SET i = 0;
WHILE i < citiesAmount DO
    SELECT id, latlon INTO currentCityId, currentCityLatlon FROM Cities LIMIT i,1;
    SELECT id FROM Venues WHERE (assignedCity IS NULL AND MBRContains (ST_Buffer(currentCityLatlon, %s), latlon));
    SET i = i + 1;
END WHILE;
END"""

assign_query = """CREATE PROCEDURE AssignCities()
BEGIN
DECLARE citiesAmount INT;
DECLARE i INT;
DECLARE currentCityId INT;
DECLARE currentCityLatlon POINT;
SELECT COUNT(id) FROM Cities INTO citiesAmount;
SET i = 0;
WHILE i < citiesAmount DO
    SELECT id, latlon INTO currentCityId, currentCityLatlon FROM Cities LIMIT i,1;
    UPDATE Venues SET assignedCity = currentCityId WHERE (assignedCity IS NULL AND MBRContains (ST_Buffer(currentCityLatlon, %s), latlon));
    SET i = i + 1;
END WHILE;
END"""

has_null_query = "SELECT count(id) FROM Venues WHERE assignedCity IS NULL;"
drop_assign_procedure = "DROP PROCEDURE IF EXISTS AssignCities;"
drop_test_procedure = "DROP PROCEDURE IF EXISTS TestCities;"

def strip_nullbytes(v):
    return hex(int(v[0].rstrip('\x00')))

def create_call_test_proc(distance):
    cursor_drop_test_proc = mysqldb_connection.cursor()
    cursor_drop_test_proc.execute(drop_test_procedure)
    mysqldb_connection.commit()
    cursor_drop_test_proc.close()

    cursor = mysqldb_connection.cursor()
    cursor.execute(test_query, (distance,))
    cursor.close()

    cursor = mysqldb_connection.cursor()
    cursor.callproc("TestCities")
    #mysqldb_connection.commit()
    venue_ids = []
    for result in cursor.stored_results():
        venue_ids.extend(map(strip_nullbytes, result.fetchall()))
    cursor.close()
    return [item for item, count in collections.Counter(venue_ids).items() if count > 1]

def create_call_assign_proc(distance):
    cursor_drop_assign_proc = mysqldb_connection.cursor()
    cursor_drop_assign_proc.execute(drop_assign_procedure)
    mysqldb_connection.commit()
    cursor_drop_assign_proc.close()

    cursor = mysqldb_connection.cursor()
    cursor.execute(assign_query, (distance,))
    cursor.close()

    cursor = mysqldb_connection.cursor()
    cursor.callproc("AssignCities")
    #mysqldb_connection.commit()
    venue_ids = []
    for result in cursor.stored_results():
        venue_ids.extend(map(strip_nullbytes, result.fetchall()))
    cursor.close()
    return [item for item, count in collections.Counter(venue_ids).items() if count > 1]

with open("data/sorted_distances.txt", 'r') as distances_file:
    for value in distances_file:
        distance = float(value.rstrip())
        cursor_null = mysqldb_connection.cursor()
        cursor_null.execute(has_null_query)
        number_of_null = cursor_null.fetchone()[0]
        cursor_null.close()
        if(number_of_null < 1):
            break
        duplicate_venues = [hex(1)]
        i = 0
        while (len(duplicate_venues) > 0):
            dist = distance/(2 + 0.1*i)
            duplicate_venues = create_call_test_proc(dist)
            i += 1
        create_call_assign_proc(dist)
    mysqldb_connection.close()