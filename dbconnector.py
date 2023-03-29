import mysql.connector
from mysql.connector import Error

try:
    host = input("Database IP:")  # use localhost for localhosted
    database = input("Database:")
    user = input("Username:")  # use root for root
    password = input("Password:")

    connection = mysql.connector.connect(host=host,
                                         database=database,
                                         user=user,
                                         password=password)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

    print("avaliable tables to work on:")
    cursor = connection.cursor()
    cursor.execute("show tables;")
    record = cursor.fetchall()
    print(record)

    cursor = connection.cursor()

    playerid = input("Player ID:")
    tableid = input("Table exact name:")

    print("Before updating a record")
    sql_select_query = "select * from " + \
        str(tableid) + " where id = {0}".format(playerid)
    cursor.execute(sql_select_query)
    record = cursor.fetchone()
    print(record)

    newvalue = input("Updated value:")
    row = input("Row selected for new value:")

    sql_update_query = "update " + \
        str(tableid) + " set " + str(row) + " = " + str(newvalue) + \
        " where id = {0}".format(playerid)
    cursor.execute(sql_update_query)
    connection.commit()
    print("record updated!")

    print("After updating a record")
    cursor.execute(sql_select_query)
    record = cursor.fetchone()
    print(record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
