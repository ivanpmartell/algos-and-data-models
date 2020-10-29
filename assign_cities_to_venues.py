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
    return [item for item, count in collections.Counter(venue_ids).items() if count > 1], len(venue_ids)

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
    mysqldb_connection.commit()
    cursor.close()

def venues_unassigned():
    cursor_null = mysqldb_connection.cursor()
    cursor_null.execute(has_null_query)
    number_of_null = cursor_null.fetchone()[0]
    cursor_null.close()
    return number_of_null

distances_stack = []
with open("data/sorted_distances.txt", 'r') as distances_file:
    for line in distances_file:
        distances_stack.append(float(line.rstrip()))
    distances_stack.append(float(0))

i = 1
while (True):
    try:
        distance = distances_stack.pop()
    except:
        break
    if(venues_unassigned() < 1):
        break

    duplicate_venues, amount_of_venues = create_call_test_proc(distance)
    print(f"Step {i}")
    print(f"{len(duplicate_venues)} ambiguous venue's cities left")
    print(f"{amount_of_venues} venues within latlon distance: {distance}")
    if amount_of_venues > 0:
        if len(duplicate_venues) == 0:
            create_call_assign_proc(distance)
            print(f"{amount_of_venues} have been assigned to a city")
            previous_distance = distance
        else:
            new_distance = (distance + previous_distance) / 2
            print(f"Ambiguous city for venues. Adding distance to stack: {new_distance}")
            distances_stack.append(distance)
            distances_stack.append(new_distance)
    else:
        previous_distance = distance
    print("Moving to next distance")
    i += 1
        
mysqldb_connection.close()