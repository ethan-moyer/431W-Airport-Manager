from PySide6 import QtCore, QtWidgets, QtGui

class SignIn(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Airport Manager - Sign In")

        self.managerLabel = QtWidgets.QLabel("Airport Manager", alignment = QtCore.Qt.AlignCenter)
        managerFont = QtGui.QFont()
        managerFont.setPointSize(26)
        managerFont.setBold(True)
        self.managerLabel.setFont(managerFont)

        self.descriptionLabel = QtWidgets.QLabel("Please select the type of user", alignment = QtCore.Qt.AlignCenter)
        self.passengerButton = QtWidgets.QPushButton("Passenger")
        self.passengerButton.clicked.connect(self.check_size)
        self.crewButton = QtWidgets.QPushButton("Crew")
        self.adminButton = QtWidgets.QPushButton("Admin")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addStretch()
        self.layout.addWidget(self.managerLabel)
        self.layout.addWidget(self.descriptionLabel)
        self.layout.addWidget(self.passengerButton)
        self.layout.addWidget(self.crewButton)
        self.layout.addWidget(self.adminButton)
        self.layout.addStretch()

        self.resize(350, 370)

    @QtCore.Slot()
    def check_size(self):
        print(self.size())