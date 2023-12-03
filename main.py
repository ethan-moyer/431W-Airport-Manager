import sys
from PySide6 import QtSql
from PySide6.QtWidgets import QApplication

from sign_in import UserTypeDialog, SignInDialog
from passenger import PassengerWindow
from crew import CrewWindow
from admin import AdminWindow

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
    app = QApplication(sys.argv)

    db = QtSql.QSqlDatabase.addDatabase("QPSQL")
    db.setHostName("localhost")
    db.setDatabaseName("airport_manager")
    db.setUserName("postgres")
    db.setPassword("airport123")
    ok = db.open()

    if not ok:
        print("NOT ABLE TO LOAD DATABASE:")
        print(f"Last error: {db.lastError().text()}")
        print(f"{QtSql.QSqlDatabase.drivers()=}")
        raise Exception("Couldn't load database")

    # view_database_info(db)

    userTypeDialog = UserTypeDialog()

    if userTypeDialog.exec() == 1:
        mode = userTypeDialog.mode
        signInDialog = SignInDialog(mode)

        if signInDialog.exec() == 1:
            if mode == 0:
                user_pid = signInDialog.id
                print(f"user_pid is {user_pid}")

                passengerWindow = PassengerWindow(user_pid)
                passengerWindow.show()
            elif mode == 1:
                crew_pid = signInDialog.id
                print(f"crew_pid is {crew_pid}")
                crewWindow = CrewWindow(crew_pid)
                crewWindow.show()
            else:
                adminWindow = AdminWindow()
                adminWindow.show()
            sys.exit(app.exec())