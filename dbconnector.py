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
    return details[arg]


try:
    host = cfg_read('host')
    database = cfg_read('database')
    user = cfg_read('user')
    password = cfg_read('password')
except:
    host = '0'
    database = '0'
    user = '0'
    password = '0'


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
                                             password=password
                                             )

        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(
                f"Connected to MySQL Server version {db_Info}", f"You're connected to database: {record}")
            # print("avaliable tables to work on:")
            # cursor.execute("show tables;")
            # record = cursor.fetchall()
            # print(record)
        return (True, f"Connected to MySQL Server version {db_Info}", f"You're connected to database: {record}")
    except Error as e:
        return (False, "Something went wrong: {}".format(e))


def disconnectdb():
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


def storedb(host, database, user, password):

    connection = connectdb(host, database, user, password)

    if connection[0] == True:
        cfg_save('db.cfg', f"{host}", f"{database}", f"{user}", f"{password}")
        return (True, connection[1])
    else:
        return (False, connection[1])


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
    return output


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
    except Error as err:
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

    connectdb(host, database, user, password)
    cursor = connection.cursor()
    cursor.execute("show tables;")
    records = cursor.fetchall()
    disconnectdb()
    output = []
    for record in records:
        for value in record:
            output.append(value)
    return output


def list_columns(tableid, host, database, user, password):
    connectdb(host, database, user, password)
    cursor = connection.cursor()
    cursor.execute(
        f"select column_name from information_schema.columns where table_schema = '{database}' and table_name = '{tableid}';")
    records = cursor.fetchall()
    disconnectdb()
    output = []
    for record in records:
        for value in record:
            output.append(value)
    return output


def updatedb(tableid, sortby, sortvalue, row, newvalue, host, database, user, password):
    connectdb(host, database, user, password)
    cursor = connection.cursor(dictionary=True)

    sql_select_query = f"select * from {tableid} where {sortby} = '{sortvalue}'"

    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    output = defaultdict(list)
    for record in records:
        for key, value in record.items():
            output[key].append(value)
    print(output)

    sql_update_query = f"update {tableid} set {row} = {newvalue} where {sortby} = '{sortvalue}'"

    cursor.execute(sql_update_query)
    connection.commit()

    # cursor.execute(sql_select_query)
    disconnectdb()
    return output
