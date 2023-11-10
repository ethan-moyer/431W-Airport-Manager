from PySide6 import QtCore, QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Click Me!")
        self.text = QtWidgets.QLabel("Hello!", alignment = QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.button_clicked)

    @QtCore.Slot()
    def button_clicked(self):
        self.text.setText("World")
