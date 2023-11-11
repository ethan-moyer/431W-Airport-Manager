from ctypes import alignment
from PySide6 import QtCore, QtWidgets, QtGui

class UserTypeDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.mode = 0

        self.setWindowTitle("Airport Manager - Select User Type")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addStretch()

        managerLabel = QtWidgets.QLabel("Airport Manager", alignment = QtCore.Qt.AlignCenter)
        managerFont = QtGui.QFont()
        managerFont.setPointSize(26)
        managerFont.setBold(True)
        managerLabel.setFont(managerFont)
        self.layout.addWidget(managerLabel)

        descriptionLabel = QtWidgets.QLabel("Please select the type of user", alignment = QtCore.Qt.AlignCenter)
        self.layout.addWidget(descriptionLabel)

        self.buttonMapper = QtCore.QSignalMapper()
        self.buttonMapper.mappedInt.connect(self.setMode)

        self.passengerButton = QtWidgets.QPushButton("Passenger")
        self.passengerButton.clicked.connect(self.buttonMapper.map)
        self.buttonMapper.setMapping(self.passengerButton, 0)
        self.layout.addWidget(self.passengerButton)

        self.crewButton = QtWidgets.QPushButton("Crew")
        self.crewButton.clicked.connect(self.buttonMapper.map)
        self.buttonMapper.setMapping(self.crewButton, 1)
        self.layout.addWidget(self.crewButton)

        self.adminButton = QtWidgets.QPushButton("Admin")
        self.adminButton.clicked.connect(self.buttonMapper.map)
        self.buttonMapper.setMapping(self.adminButton, 2)
        self.layout.addWidget(self.adminButton)

        self.layout.addStretch()
        self.resize(350, 370)

    @QtCore.Slot(int)
    def setMode(self, newMode: int) -> None:
        self.mode = newMode
        self.accept()

class SignInDialog(QtWidgets.QDialog):
    def __init__(self, mode: int) -> None:
        super().__init__()

        self.mode = mode

        self.setWindowTitle("Airport Manager - Sign In")

        self.layout = QtWidgets.QStackedLayout(self)

        self.signInWidget = QtWidgets.QWidget()
        self.layout.addWidget(self.signInWidget)
        self.signInLayout = QtWidgets.QFormLayout(self.signInWidget)

        self.signUpWidget = QtWidgets.QWidget()
        self.layout.addWidget(self.signUpWidget)
        self.signUpLayout = QtWidgets.QFormLayout(self.signUpWidget)

        # Sign In Layout
        signInLabel = QtWidgets.QLabel("Sign In", alignment=QtCore.Qt.AlignCenter)
        signInFont = QtGui.QFont()
        signInFont.setPointSize(18)
        signInLabel.setFont(signInFont)
        self.signInLayout.addRow(signInLabel)

        self.signInUsernameLineEdit = QtWidgets.QLineEdit()
        self.signInLayout.addRow("Username:", self.signInUsernameLineEdit)

        self.signInPasswordLineEdit = QtWidgets.QLineEdit()
        self.signInPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signInLayout.addRow("Password:", self.signInPasswordLineEdit)

        self.signInButton = QtWidgets.QPushButton("Sign In")
        self.signInButton.clicked.connect(self.signInButtonClicked)
        self.signInLayout.addRow(self.signInButton)

        # Sign Up Layout
        self.signUpButton = QtWidgets.QPushButton("Create New Account")
        if self.mode == 0:
            self.signInLayout.addRow(self.signUpButton)
            self.signUpButton.clicked.connect(self.signUpButtonClicked)

        signUpLabel = QtWidgets.QLabel("Sign Up", alignment=QtCore.Qt.AlignCenter)
        signUpLabel.setFont(signInFont)
        self.signUpLayout.addRow(signUpLabel)

        self.firstNameLineEdit = QtWidgets.QLineEdit()
        self.signUpLayout.addRow("First Name:", self.firstNameLineEdit)

        self.lastNameLineEdit = QtWidgets.QLineEdit()
        self.signUpLayout.addRow("Last Name:", self.lastNameLineEdit)

        self.dobDateEdit = QtWidgets.QDateEdit()
        self.signUpLayout.addRow("Date of Birth:", self.dobDateEdit)

        self.signUpUsernameLineEdit = QtWidgets.QLineEdit()
        self.signUpLayout.addRow("Username:", self.signUpUsernameLineEdit)

        self.signUpPasswordLineEdit = QtWidgets.QLineEdit()
        self.signUpPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signUpLayout.addRow("Password:", self.signUpPasswordLineEdit)

        self.createAccountButton = QtWidgets.QPushButton("Create Account")
        self.createAccountButton.clicked.connect(self.createAccountButtonClicked)
        self.signUpLayout.addRow(self.createAccountButton)

        self.resize(350, 150)

    @QtCore.Slot()
    def signInButtonClicked(self):
        print("Check username/password here")

    @QtCore.Slot()
    def signUpButtonClicked(self):
        self.setWindowTitle("Airport Manager - Sign Up")
        self.layout.setCurrentIndex(1)

    @QtCore.Slot()
    def createAccountButtonClicked(self):
        print("Create account here")
