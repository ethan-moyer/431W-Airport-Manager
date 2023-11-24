import sys
from PySide6 import QtSql
from PySide6.QtWidgets import QApplication

def initDatabase():
    app = QApplication(sys.argv)
    
    db = QtSql.QSqlDatabase.addDatabase("QMARIADB")
    db.setHostName("localhost")
    db.setDatabaseName("sys")
    db.setUserName("root")
    db.setPassword("airport123")
    ok = db.open()

    assert(ok)

    query = QtSql.QSqlQuery(db)

    # Remove existing data
    query.exec("DROP DATABASE IF EXISTS airport_manager;")

    # Create and switch to new database
    query.exec("CREATE DATABASE airport_manager;")
    query.exec("USE airport_manager;")

    # Create tables
    query.exec("CREATE TABLE Passengers(\
                pid INT AUTO_INCREMENT,\
                fname VARCHAR(31) NOT NULL,\
                lname VARCHAR(31) NOT NULL,\
                dob DATE NOT NULL,\
                PRIMARY KEY (pid));")

    query.exec("CREATE TABLE Crew(\
                cid INT AUTO_INCREMENT,\
                fname VARCHAR(31) NOT NULL,\
                lname VARCHAR(31) NOT NULL,\
                dob DATE NOT NULL,\
                position VARCHAR(31) NOT NULL,\
                PRIMARY KEY (cid)\
                );")

    query.exec("CREATE TABLE Airlines(\
                aid INT AUTO_INCREMENT,\
                name VARCHAR(31) NOT NULL,\
                PRIMARY KEY (aid)\
                );")

    query.exec("CREATE TABLE Models(\
                model_name VARCHAR(31) NOT NULL,\
                capacity INT NOT NULL,\
                PRIMARY KEY (model_name)\
                );")

    query.exec("CREATE TABLE Planes(\
                plane_id INT AUTO_INCREMENT,\
                model_name VARCHAR(31) NOT NULL,\
                aid INT,\
                PRIMARY KEY (plane_id),\
                FOREIGN KEY (model_name) REFERENCES Models(model_name)\
                ON UPDATE CASCADE ON DELETE CASCADE,\
                FOREIGN KEY (aid) REFERENCES Airlines(aid)\
                ON UPDATE CASCADE ON DELETE SET NULL\
                );")

    query.exec("CREATE TABLE Schedule(\
                fid INT AUTO_INCREMENT,\
                plane_id INT NOT NULL,\
                dep_term VARCHAR(3) NOT NULL,\
                dep_time DATETIME NOT NULL,\
                arr_term VARCHAR(3) NOT NULL,\
                arr_time DATETIME NOT NULL,\
                dest_airport VARCHAR(3) NOT NULL,\
                PRIMARY KEY (fid),\
                FOREIGN KEY (plane_id) REFERENCES Planes(plane_id)\
                ON UPDATE CASCADE ON DELETE CASCADE\
                );")

    query.exec("CREATE TABLE Bags(\
                bid INT AUTO_INCREMENT,\
                pid INT NOT NULL,\
                fid INT NOT NULL,\
                PRIMARY KEY (bid),\
                FOREIGN KEY (pid) REFERENCES Passengers(pid)\
                ON UPDATE RESTRICT ON DELETE CASCADE,\
                FOREIGN KEY (fid) REFERENCES Schedule(fid)\
                ON UPDATE RESTRICT ON DELETE CASCADE)")
    
    query.exec("CREATE TABLE Bookings(\
                pid INT NOT NULL,\
                fid INT NOT NULL,\
                seat_num INT NOT NULL,\
                PRIMARY KEY (pid, fid),\
                FOREIGN KEY (pid) REFERENCES Passengers(pid)\
                ON UPDATE RESTRICT ON DELETE CASCADE,\
                FOREIGN KEY (fid) REFERENCES Schedule(fid)\
                ON UPDATE RESTRICT ON DELETE CASCADE,\
                UNIQUE (fid, seat_num))")

    query.exec("CREATE TABLE CrewBookings(\
                cid INT NOT NULL,\
                fid INT NOT NULL,\
                PRIMARY KEY (cid, fid),\
                FOREIGN KEY (cid) REFERENCES Crew(cid)\
                ON UPDATE RESTRICT ON DELETE CASCADE,\
                FOREIGN KEY (fid) REFERENCES Schedule(fid)\
                ON UPDATE RESTRICT ON DELETE CASCADE\
                );")

    db.close()
    QtSql.QSqlDatabase.removeDatabase("sys")

if __name__ == "__main__":
    initDatabase()