import sys
from PySide6.QtWidgets import QApplication

from my_widget import MyWidget
from sign_in import UserTypeDialog, SignInDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = UserTypeDialog()

    if widget.exec() == 1:
        print(widget.mode)

        widget2 = SignInDialog(widget.mode)
        widget2.show()

        sys.exit(app.exec())
