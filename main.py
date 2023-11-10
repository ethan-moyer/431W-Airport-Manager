import sys
from PySide6.QtWidgets import QApplication

from my_widget import MyWidget
from sign_in import SignIn

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = SignIn()
    widget.show()

    sys.exit(app.exec())
