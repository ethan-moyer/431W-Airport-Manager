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

        passengerButton = QtWidgets.QPushButton("Passenger")
        passengerButton.clicked.connect(self.buttonMapper.map)
        self.buttonMapper.setMapping(passengerButton, 0)
        self.layout.addWidget(passengerButton)

        crewButton = QtWidgets.QPushButton("Crew")
        crewButton.clicked.connect(self.buttonMapper.map)
        self.buttonMapper.setMapping(crewButton, 1)
        self.layout.addWidget(crewButton)

        adminButton = QtWidgets.QPushButton("Admin")
        adminButton.clicked.connect(self.buttonMapper.map)
        self.buttonMapper.setMapping(adminButton, 2)
        self.layout.addWidget(adminButton)

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

        signInWidget = QtWidgets.QWidget()
        self.layout.addWidget(signInWidget)
        signInLayout = QtWidgets.QFormLayout(signInWidget)

        signUpWidget = QtWidgets.QWidget()
        self.layout.addWidget(signUpWidget)
        signUpLayout = QtWidgets.QFormLayout(signUpWidget)

        # Sign In Layout
        signInLabel = QtWidgets.QLabel("Sign In", alignment=QtCore.Qt.AlignCenter)
        signInFont = QtGui.QFont()
        signInFont.setPointSize(18)
        signInLabel.setFont(signInFont)
        signInLayout.addRow(signInLabel)

        self.signInUsernameLineEdit = QtWidgets.QLineEdit()
        signInLayout.addRow("Username:", self.signInUsernameLineEdit)

        self.signInPasswordLineEdit = QtWidgets.QLineEdit()
        self.signInPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        signInLayout.addRow("Password:", self.signInPasswordLineEdit)

        signInButton = QtWidgets.QPushButton("Sign In")
        signInButton.clicked.connect(self.signInButtonClicked)
        signInLayout.addRow(signInButton)

        # Sign Up Layout
        signUpButton = QtWidgets.QPushButton("Create New Account")
        if self.mode == 0:
            signInLayout.addRow(signUpButton)
            signUpButton.clicked.connect(self.signUpButtonClicked)

        signUpLabel = QtWidgets.QLabel("Sign Up", alignment=QtCore.Qt.AlignCenter)
        signUpLabel.setFont(signInFont)
        signUpLayout.addRow(signUpLabel)

        self.firstNameLineEdit = QtWidgets.QLineEdit()
        signUpLayout.addRow("First Name:", self.firstNameLineEdit)

        self.lastNameLineEdit = QtWidgets.QLineEdit()
        signUpLayout.addRow("Last Name:", self.lastNameLineEdit)

        self.dobDateEdit = QtWidgets.QDateEdit()
        signUpLayout.addRow("Date of Birth:", self.dobDateEdit)

        self.signUpUsernameLineEdit = QtWidgets.QLineEdit()
        signUpLayout.addRow("Username:", self.signUpUsernameLineEdit)

        self.signUpPasswordLineEdit = QtWidgets.QLineEdit()
        self.signUpPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        signUpLayout.addRow("Password:", self.signUpPasswordLineEdit)

        createAccountButton = QtWidgets.QPushButton("Create Account")
        createAccountButton.clicked.connect(self.createAccountButtonClicked)
        signUpLayout.addRow(createAccountButton)

        self.resize(350, 150)

    @QtCore.Slot()
    def signInButtonClicked(self) -> None:
        print("Check username/password here")
        self.accept()

    @QtCore.Slot()
    def signUpButtonClicked(self) -> None:
        self.setWindowTitle("Airport Manager - Sign Up")
        self.layout.setCurrentIndex(1)

    @QtCore.Slot()
    def createAccountButtonClicked(self) -> None:
        print("Create account here")
        self.accept()
