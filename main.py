import sys
from PySide6 import QtSql
from PySide6.QtWidgets import QApplication

from sign_in import UserTypeDialog, SignInDialog
from passenger import PassengerWindow
from crew import CrewWindow
from admin import AdminWindow

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


    userTypeDialog = UserTypeDialog()

    if userTypeDialog.exec() == 1:
        mode = userTypeDialog.mode
        signInDialog = SignInDialog(mode)

        if signInDialog.exec() == 1:
            if mode == 0:
                passengerWindow = PassengerWindow()
                passengerWindow.show()
            elif mode == 1:
                crewWindow = CrewWindow()
                crewWindow.show()
            else:
                adminWindow = AdminWindow()
                adminWindow.show()

            sys.exit(app.exec())
