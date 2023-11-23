from PySide6 import QtCore, QtWidgets, QtSql

class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager")

        tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(tabWidget)

        flightsTab = QtWidgets.QWidget()
        tabWidget.addTab(flightsTab, "Flights")

        passengersTab = QtWidgets.QWidget()
        tabWidget.addTab(passengersTab, "Passengers")

        crewTab = QtWidgets.QWidget()
        tabWidget.addTab(crewTab, "Crew")

        # Flights tab
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

        self.flightDetailsButton = QtWidgets.QPushButton("View Details")
        self.flightDetailsButton.clicked.connect(self.openDetailsDialog)
        flightsButtonLayout.addWidget(self.flightDetailsButton)

        self.removeFlightButton = QtWidgets.QPushButton("Remove Flight")
        self.removeFlightButton.clicked.connect(self.removeFlight)
        flightsButtonLayout.addWidget(self.removeFlightButton)

        self.resize(1120, 590)

    @QtCore.Slot()
    def openDetailsDialog(self) -> None:
        details = FlightDetailsDialog()
        details.exec()

    @QtCore.Slot()
    def removeFlight(self) -> None:
        print("Remove flight here")

class FlightDetailsDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Flight Details")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(QtWidgets.QLabel("Flight ID: "))
        self.layout.addWidget(QtWidgets.QLabel("Airline: "))
        self.layout.addWidget(QtWidgets.QLabel("Plane: "))
        self.layout.addWidget(QtWidgets.QLabel("Terminal: "))
        self.layout.addWidget(QtWidgets.QLabel("Departure Date: "))
        self.layout.addWidget(QtWidgets.QLabel("Departure Time: "))
        self.layout.addWidget(QtWidgets.QLabel("Arrival Time: "))
        self.layout.addWidget(QtWidgets.QLabel("Destination: "))

        self.layout.addStretch()

        self.layout.addWidget(QtWidgets.QLabel("Passengers:"))
        passengersModel = QtSql.QSqlQueryModel()
        passengersView = QtWidgets.QTableView()
        passengersView.setModel(passengersModel)
        self.layout.addWidget(passengersView)

        passengersButtonLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(passengersButtonLayout)
        passengersButtonLayout.addStretch()

        self.addPassengerButton = QtWidgets.QPushButton("Add Passenger")
        self.addPassengerButton.clicked.connect(self.addPassenger)
        passengersButtonLayout.addWidget(self.addPassengerButton)

        self.removePassengerButton = QtWidgets.QPushButton("Remove Passenger")
        self.removePassengerButton.clicked.connect(self.removePassenger)
        passengersButtonLayout.addWidget(self.removePassengerButton)
        
        self.layout.addStretch()

        self.layout.addWidget(QtWidgets.QLabel("Crew:"))
        crewModel = QtSql.QSqlQueryModel()
        crewView = QtWidgets.QTableView()
        crewView.setModel(crewModel)
        self.layout.addWidget(crewView)

        crewButtonLayout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(crewButtonLayout)
        crewButtonLayout.addStretch()

        self.addCrewButton = QtWidgets.QPushButton("Add Crew")
        self.addCrewButton.clicked.connect(self.addCrew)
        crewButtonLayout.addWidget(self.addCrewButton)

        self.removeCrewButton = QtWidgets.QPushButton("Remove Crew")
        self.removeCrewButton.clicked.connect(self.removeCrew)
        crewButtonLayout.addWidget(self.removeCrewButton)

        self.resize(450, 630)

    @QtCore.Slot()
    def addPassenger(self) -> None:
        print("Add passenger here")

    @QtCore.Slot()
    def removePassenger(self) -> None:
        print("Remove passenger here")

    @QtCore.Slot()
    def addCrew(self) -> None:
        print("Add crew here")

    @QtCore.Slot()
    def removeCrew(self) -> None:
        print("Remove crew here")
