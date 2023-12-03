import sys, os, csv
from PySide6 import QtSql
from PySide6.QtWidgets import QApplication

def initDatabase():
    app = QApplication(sys.argv)

    db = QtSql.QSqlDatabase.addDatabase("QPSQL")
    db.setHostName("localhost")
    db.setDatabaseName("postgres")
    db.setUserName("postgres")
    db.setPassword("airport123")
    ok = db.open()

    query = QtSql.QSqlQuery(db)

    run_query(query, "DROP DATABASE IF EXISTS airport_manager;")
    run_query(query, "CREATE DATABASE airport_manager;")

    db.close()
    QtSql.QSqlDatabase.removeDatabase("postgres")

    db.setDatabaseName("airport_manager")
    db.open()
    assert ok

    print("DATABASE CLEARED")

    # Create tables
    # Passengers Table
    run_query(query, "CREATE TABLE Passengers(\
                pid SERIAL PRIMARY KEY,\
                fname VARCHAR(31) NOT NULL,\
                lname VARCHAR(31) NOT NULL,\
                uname VARCHAR(31) UNIQUE NOT NULL, \
                pswd VARCHAR(31) NOT NULL, \
                dob DATE NOT NULL);")

    copy_table(query, 'passengers.csv', 'Passengers', 'pid')

    # Crew Table
    run_query(query, "CREATE TABLE Crew(\
                cid SERIAL PRIMARY KEY,\
                fname VARCHAR(31) NOT NULL,\
                lname VARCHAR(31) NOT NULL,\
                uname VARCHAR(31) UNIQUE NOT NULL, \
                pswd VARCHAR(31) NOT NULL, \
                dob DATE NOT NULL,\
                position VARCHAR(31) NOT NULL);")
    copy_table(query, 'crew.csv', 'Crew', 'cid')


    # Airlines Table
    run_query(query, "CREATE TABLE Airlines(\
                aid SERIAL PRIMARY KEY,\
                name VARCHAR(31) NOT NULL);")
    copy_table(query, 'airlines.csv', 'Airlines', 'aid')
    

    # Models Table
    run_query(query, "CREATE TABLE Models(\
                model_name VARCHAR(31) PRIMARY KEY,\
                capacity INT NOT NULL);")
    copy_table(query, 'models.csv', 'Models', None)

    # Planes Table
    run_query(query, "CREATE TABLE Planes(\
                plane_id SERIAL PRIMARY KEY,\
                model_name VARCHAR(31) NOT NULL REFERENCES Models(model_name) ON UPDATE CASCADE ON DELETE CASCADE,\
                aid INT REFERENCES Airlines(aid) ON UPDATE CASCADE ON DELETE SET NULL);")
    copy_table(query, 'planes.csv', 'Planes', 'plane_id')

    # Schedule Table
    run_query(query, "CREATE TABLE Schedule(\
                fid SERIAL PRIMARY KEY,\
                plane_id INT NOT NULL REFERENCES Planes(plane_id) ON UPDATE CASCADE ON DELETE CASCADE,\
                dep_term VARCHAR(3) NOT NULL,\
                dep_time TIMESTAMP NOT NULL,\
                arr_term VARCHAR(3) NOT NULL,\
                arr_time TIMESTAMP NOT NULL,\
                dest_airport VARCHAR(3) NOT NULL);")
    copy_table(query, 'schedule.csv', 'Schedule', 'fid')

    # Bags Table
    run_query(query, "CREATE TABLE Bags(\
                bid SERIAL PRIMARY KEY,\
                pid INT NOT NULL REFERENCES Passengers(pid) ON UPDATE RESTRICT ON DELETE CASCADE,\
                fid INT NOT NULL REFERENCES Schedule(fid) ON UPDATE RESTRICT ON DELETE CASCADE);")
    copy_table(query, 'bags.csv', 'Bags', 'bid')

    # Bookings Table
    run_query(query, "CREATE TABLE Bookings(\
                pid INT NOT NULL,\
                fid INT NOT NULL,\
                seat_num INT NOT NULL,\
                PRIMARY KEY (pid, fid),\
                FOREIGN KEY (pid) REFERENCES Passengers(pid) ON UPDATE RESTRICT ON DELETE CASCADE,\
                FOREIGN KEY (fid) REFERENCES Schedule(fid) ON UPDATE RESTRICT ON DELETE CASCADE,\
                UNIQUE (fid, seat_num));")
    copy_table(query, 'bookings.csv', 'Bookings', None)

    # CrewBookings Table
    run_query(query, "CREATE TABLE CrewBookings(\
                cid INT NOT NULL,\
                fid INT NOT NULL,\
                PRIMARY KEY (cid, fid),\
                FOREIGN KEY (cid) REFERENCES Crew(cid) ON UPDATE RESTRICT ON DELETE CASCADE,\
                FOREIGN KEY (fid) REFERENCES Schedule(fid) ON UPDATE RESTRICT ON DELETE CASCADE);")
    copy_table(query, 'crew_bookings.csv', 'CrewBookings', None)


    print("ALL QUERIES RAN SUCCESSFULLY.")
    # view_database_info(db)

    db.close()
    QtSql.QSqlDatabase.removeDatabase("airport_manager")

def run_query(query, query_text):
    result = query.exec(query_text)
    if not result:
        print(f"FAILED TO RUN \n{query_text}\n\n")
        print(f"ERROR: {query.lastError()}")
        raise Exception("Database failure")
            
import codecs

def remove_bom(s):
    return s.lstrip(codecs.BOM_UTF8.decode('utf-8'))

def reset_serial_sequence(query, table_name, primary_key_column):
    max_id_query = f"SELECT MAX({primary_key_column}) FROM {table_name}"
    query.exec(max_id_query)
    if query.next():
        max_id = query.value(0) or 0  # Handle None case
    else:
        max_id = 0
    reset_seq_query = f"SELECT setval('{table_name}_{primary_key_column}_seq', {max_id + 1}, false)"
    if not query.exec(reset_seq_query):
        print(f"Error resetting sequence for {table_name}: {query.lastError().text()}")


def copy_table(query, csv_file_path, table_name, primary_key_column, real_data=True):
    with open('real_data/'*real_data+csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        # Can't figure out why these characters sometimes exist
        # But this does fix it
        headers = [remove_bom(header) for header in headers]
        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['?'] * len(headers))})"
        for row in reader:
            query.prepare(insert_query)
            for i, value in enumerate(row):
                query.bindValue(i, value)
            if not query.exec():
                print(f"Failed to insert row: {row}")
                print(f"Error: {query.lastError().text()}")
                break
    if primary_key_column:
        reset_serial_sequence(query, table_name, primary_key_column)


def view_database_info(db):
    table_query = QtSql.QSqlQuery(db)
    table_query.exec("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")

    while table_query.next():
        table_name = table_query.value(0)
        print_table(db, table_name)
        print("\n"+"-"*20+"\n")

def print_table(db, table_name):
    table_query2 = QtSql.QSqlQuery(db)

    table_query2.exec(f"SELECT * FROM {table_name}")
    record = table_query2.record()

    # Get column names
    column_names = [record.fieldName(i) for i in range(record.count())]
    print(f"TABLE: {table_name}")
    print("Column Names:", column_names)
    while table_query2.next():
        row_values = [table_query2.value(i) for i in range(table_query2.record().count())]
        print(row_values)

if __name__ == "__main__":
    initDatabase()