from PySide6 import QtCore, QtWidgets, QtSql

class PassengerWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager")

        tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(tabWidget)

        flightsTab = QtWidgets.QWidget()
        tabWidget.addTab(flightsTab, "Flights")

        bookingsTab = QtWidgets.QWidget()
        tabWidget.addTab(bookingsTab, "Bookings")

        flightsVLayout = QtWidgets.QVBoxLayout(flightsTab)
        flightsHLayout = QtWidgets.QHBoxLayout()
        flightsVLayout.addLayout(flightsHLayout)

        flightsHLayout.addWidget(QtWidgets.QLabel("From:"))
        self.fromDateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.fromDateEdit.setMinimumWidth(100)
        flightsHLayout.addWidget(self.fromDateEdit)
        self.fromCheckBox = QtWidgets.QCheckBox()
        flightsHLayout.addWidget(self.fromCheckBox)

        flightsHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        flightsHLayout.addWidget(QtWidgets.QLabel("To:"))
        self.toDateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addDays(14))
        self.toDateEdit.setMinimumWidth(100)
        flightsHLayout.addWidget(self.toDateEdit)
        self.toCheckBox = QtWidgets.QCheckBox()
        flightsHLayout.addWidget(self.toCheckBox)

        flightsHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        flightsHLayout.addWidget(QtWidgets.QLabel("Airline:"))
        self.airlineComboBox = QtWidgets.QComboBox()
        self.airlineComboBox.setMinimumWidth(150)
        flightsHLayout.addWidget(self.airlineComboBox)

        flightsHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        flightsHLayout.addWidget(QtWidgets.QLabel("Destination:"))
        self.destinationLineEdit = QtWidgets.QLineEdit()
        self.destinationLineEdit.setFixedWidth(70)
        flightsHLayout.addWidget(self.destinationLineEdit)

        flightsHLayout.addStretch()

        self.flightsModel = QtSql.QSqlQueryModel()
        self.flightsView = QtWidgets.QTableView()
        self.flightsView.setModel(self.flightsModel)
        flightsVLayout.addWidget(self.flightsView)

        flightsButtonLayout = QtWidgets.QHBoxLayout()
        flightsVLayout.addLayout(flightsButtonLayout)
        flightsButtonLayout.addStretch()
        self.bookFlightsButton = QtWidgets.QPushButton("Book Flight")
        self.bookFlightsButton.clicked.connect(self.openBookFlightDialog)
        flightsButtonLayout.addWidget(self.bookFlightsButton)

        self.resize(1120, 590)

    @QtCore.Slot()
    def openBookFlightDialog(self) -> None:
        bookFlightDialog = BookFlightDialog()
        if bookFlightDialog.exec():
            print("Add booking to database")

class BookFlightDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Book Flight")

        self.layout = QtWidgets.QFormLayout(self)

        self.seatNumComboBox = QtWidgets.QComboBox()
        for i in range(1, 51):
            self.seatNumComboBox.addItem(str(i))
        self.layout.addRow("Seat:", self.seatNumComboBox)

        self.bagNumComboBox = QtWidgets.QComboBox()
        for i in range(0, 3):
            self.bagNumComboBox.addItem(str(i))
        self.layout.addRow("Number of bags:", self.bagNumComboBox)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addRow(buttonBox)

        self.resize(280, 100)
