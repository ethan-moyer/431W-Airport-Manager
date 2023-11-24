import sys
from PySide6 import QtSql
from PySide6.QtWidgets import QApplication

from sign_in import UserTypeDialog, SignInDialog
from passenger import PassengerWindow
from crew import CrewWindow
from admin import AdminWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # If prints out True, can connect to database
    db = QtSql.QSqlDatabase.addDatabase("QMARIADB")
    db.setHostName("localhost")
    db.setDatabaseName("airport_manager")
    db.setUserName("root")
    db.setPassword("airport123")
    ok = db.open()
    print(ok)

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
