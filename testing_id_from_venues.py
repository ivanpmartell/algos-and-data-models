import mysql.connector as mysqldb

mysqldb_connection = mysqldb.connect(host='localhost', user='ivan', password='CSC501@ssignments', database='assignment1')

cursor = mysqldb_connection.cursor()
cursor.execute("SELECT * FROM Venues LIMIT 1;")
result = cursor.fetchone()
result_id = hex(int(result[0].rstrip('\x00')))
cursor.close()