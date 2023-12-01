import sys
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

    assert(ok)

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
                dob DATE NOT NULL);")

    # Crew Table
    run_query(query, "CREATE TABLE Crew(\
                cid SERIAL PRIMARY KEY,\
                fname VARCHAR(31) NOT NULL,\
                lname VARCHAR(31) NOT NULL,\
                dob DATE NOT NULL,\
                position VARCHAR(31) NOT NULL);")

    # Airlines Table
    run_query(query, "CREATE TABLE Airlines(\
                aid SERIAL PRIMARY KEY,\
                name VARCHAR(31) NOT NULL);")

    # Models Table
    run_query(query, "CREATE TABLE Models(\
                model_name VARCHAR(31) PRIMARY KEY,\
                capacity INT NOT NULL);")

    # Planes Table
    run_query(query, "CREATE TABLE Planes(\
                plane_id SERIAL PRIMARY KEY,\
                model_name VARCHAR(31) NOT NULL REFERENCES Models(model_name) ON UPDATE CASCADE ON DELETE CASCADE,\
                aid INT REFERENCES Airlines(aid) ON UPDATE CASCADE ON DELETE SET NULL);")

    # Schedule Table
    run_query(query, "CREATE TABLE Schedule(\
                fid SERIAL PRIMARY KEY,\
                plane_id INT NOT NULL REFERENCES Planes(plane_id) ON UPDATE CASCADE ON DELETE CASCADE,\
                dep_term VARCHAR(3) NOT NULL,\
                dep_time TIMESTAMP NOT NULL,\
                arr_term VARCHAR(3) NOT NULL,\
                arr_time TIMESTAMP NOT NULL,\
                dest_airport VARCHAR(3) NOT NULL);")

    # Bags Table
    run_query(query, "CREATE TABLE Bags(\
                bid SERIAL PRIMARY KEY,\
                pid INT NOT NULL REFERENCES Passengers(pid) ON UPDATE RESTRICT ON DELETE CASCADE,\
                fid INT NOT NULL REFERENCES Schedule(fid) ON UPDATE RESTRICT ON DELETE CASCADE);")

    # Bookings Table
    run_query(query, "CREATE TABLE Bookings(\
                pid INT NOT NULL,\
                fid INT NOT NULL,\
                seat_num INT NOT NULL,\
                PRIMARY KEY (pid, fid),\
                FOREIGN KEY (pid) REFERENCES Passengers(pid) ON UPDATE RESTRICT ON DELETE CASCADE,\
                FOREIGN KEY (fid) REFERENCES Schedule(fid) ON UPDATE RESTRICT ON DELETE CASCADE,\
                UNIQUE (fid, seat_num));")

    # CrewBookings Table
    run_query(query, "CREATE TABLE CrewBookings(\
                cid INT NOT NULL,\
                fid INT NOT NULL,\
                PRIMARY KEY (cid, fid),\
                FOREIGN KEY (cid) REFERENCES Crew(cid) ON UPDATE RESTRICT ON DELETE CASCADE,\
                FOREIGN KEY (fid) REFERENCES Schedule(fid) ON UPDATE RESTRICT ON DELETE CASCADE);")

    print("ALL QUERIES RAN SUCCESSFULLY.")
    view_database_info(db)

    db.close()
    QtSql.QSqlDatabase.removeDatabase("airport_manager")

def run_query(query, query_text):
    result = query.exec(query_text)
    if not result:
        print(f"FAILED TO RUN \n{query_text}\n\n")
        print(f"ERROR: {query.lastError()}")
        raise Exception("Database failure")

def view_database_info(db):
    table_query = QtSql.QSqlQuery(db)
    table_query.exec("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")

    print("Tables in the database:")
    while table_query.next():
        table_name = table_query.value(0)
        print(table_name)

    db.close()

if __name__ == "__main__":
    initDatabase()