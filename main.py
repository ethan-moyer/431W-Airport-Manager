import sys
from PySide6.QtWidgets import QApplication

from sign_in import UserTypeDialog, SignInDialog
from passenger import PassengerWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    userTypeDialog = UserTypeDialog()

    if userTypeDialog.exec() == 1:
        mode = userTypeDialog.mode
        signInDialog = SignInDialog(mode)

        if signInDialog.exec() == 1:
            if mode >= 0:
                passengerWindow = PassengerWindow()
                passengerWindow.show()
            
            sys.exit(app.exec())
