import configparser
import mysql.connector
from mysql.connector import Error
from collections import defaultdict
import mysql.connector.cursor_cext
from mysql.connector.cursor_cext import CMySQLCursorBuffered, List, RowType


def fetchall(self) -> List[RowType]:
    try:
        self._check_executed()
        res = self._rows[self._next_row:]
        self._next_row = len(self._rows)
        return res
    except:
        return 0


CMySQLCursorBuffered.fetchall = fetchall

# localhost = 'localhost'
# esmeralda = 'esmeralda'
# root = 'root'
# password = ''

# player_id = '1100001027c307f'
# table_id = 'summerz_accounts'
# row_id = 'whitelist'
# new_value = '0'


def connectdb(host, database, user, password):
    try:
        # host = input("Database IP:")  # use localhost for localhosted
        # database = input("Database:")
        # user = input("Username:")  # use root for root
        # password = input("Password:")
        global connection
        # global cursor

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
            # print("avaliable tables to work on:")
            # cursor.execute("show tables;")
            # record = cursor.fetchall()
            # print(record)

    except Error as e:
        print("Error while connecting to MySQL", e)


def disconnectdb():
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


def list_rows(table, host, database, user, password):
    connectdb(host, database, user, password)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"select * from {table} limit 1000;")
    records = cursor.fetchall()
    disconnectdb()
    output = defaultdict(list)
    for record in records:
        for key, value in record.items():
            output[key].append(value)
    return (output)


def run_command(command, host, database, user, password):
    try:
        connectdb(host, database, user, password)
        cursor = connection.cursor(buffered=True)
        sql_command = f"{command}"
        cursor.execute(sql_command)
        connection.commit()
        records = cursor.fetchall()
        disconnectdb()
        if records != 0:
            return sql_command, records
        else:
            return sql_command, "Command executed sucessfully "
    except mysql.connector.Error as err:
        return sql_command, ("Something went wrong: {}".format(err))


def list_unique_rows(table, playerid, host, database, user, password):
    connectdb(host, database, user, password)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"select * from {table} where steam = '{playerid}'")
    records = cursor.fetchall()
    disconnectdb()
    output = defaultdict(list)
    for record in records:
        for key, value in record.items():
            output[key].append(value)
    return output


def list_tables(host, database, user, password):
    try:
        # host = input("Database IP:")  # use localhost for localhosted
        # database = input("Database:")
        # user = input("Username:")  # use root for root
        # password = input("Password:")
        global connection
        # global cursor

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
            cursor.execute("show tables;")
            record = cursor.fetchall()
            return record

    except Error as e:
        print("Error while connecting to MySQL", e)


def list_columns(host, database, user, password, tableid):
    try:

        global connection
        # global cursor

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
            print("avaliable columns to work on:")
            # cursor.execute(f"show columns from {tableid};")
            cursor.execute(
                f"select column_name from information_schema.columns where table_schema = '{database}' and table_name = '{tableid}';")
            record = cursor.fetchall()
            return record

    except Error as e:
        print("Error while connecting to MySQL", e)


def updatedb(tableid, playerid, row, newvalue):

    cursor = connection.cursor()

    print("Before updating a record")
    sql_select_query = "select * from " + \
        str(tableid) + " where steam = '{0}'".format(playerid)
    cursor.execute(sql_select_query)
    record = cursor.fetchone()
    print(record)

    sql_update_query = "update " + \
        str(tableid) + " set " + str(row) + " = " + str(newvalue) + \
        " where steam = '{0}'".format(playerid)
    cursor.execute(sql_update_query)
    connection.commit()
    print("record updated!")

    print("After updating a record")
    cursor.execute(sql_select_query)
    record = cursor.fetchone()
    print(record)


def cfg_save(arquivo, host, database, user, password):
    with open(arquivo, 'w') as f:
        f.write("[DATA]\n")
        f.write(f"host = {host}\n")
        f.write(f"database = {database}\n")
        f.write(f"user = {user}\n")
        f.write(f"password = {password}\n")


def cfg_read(arg):
    config = configparser.RawConfigParser()
    config.read('db.cfg')
    details = dict(config.items('DATA'))
   # print(f'returned: {details[arg]}')
    return details[arg]
