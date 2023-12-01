from PySide6 import QtCore, QtWidgets, QtSql
from passenger import ModifyBookingDialog

class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager")

        tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(tabWidget)

        flightsTab = QtWidgets.QWidget()
        tabWidget.addTab(flightsTab, "Flights")

        passengersTab = QtWidgets.QTabWidget()
        tabWidget.addTab(passengersTab, "Passengers")

        crewTab = QtWidgets.QTabWidget()
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

        self.addPassengerBookingButton = QtWidgets.QPushButton("Add Passenger Booking")
        self.addPassengerBookingButton.clicked.connect(self.openPassengerBookingDialog)
        flightsButtonLayout.addWidget(self.addPassengerBookingButton)

        self.addCrewBookingButton = QtWidgets.QPushButton("Add Crew Booking")
        self.addCrewBookingButton.clicked.connect(self.openCrewBookingDialog)
        flightsButtonLayout.addWidget(self.addCrewBookingButton)

        self.addFlightButton = QtWidgets.QPushButton("Add Flight")
        self.addFlightButton.clicked.connect(self.openAddFlightDialog)
        flightsButtonLayout.addWidget(self.addFlightButton)

        self.modifyFlightButton = QtWidgets.QPushButton("Modify Flight")
        self.modifyFlightButton.clicked.connect(self.openModifyFlightDialog)
        flightsButtonLayout.addWidget(self.modifyFlightButton)

        self.removeFlightButton = QtWidgets.QPushButton("Remove Flight")
        self.removeFlightButton.clicked.connect(self.removeFlight)
        flightsButtonLayout.addWidget(self.removeFlightButton)

        # Passenger accounts tab
        passengerAccountsTab = QtWidgets.QWidget()
        passengersTab.addTab(passengerAccountsTab, "Accounts")

        paVLayout = QtWidgets.QVBoxLayout(passengerAccountsTab)
        paHLayout = QtWidgets.QHBoxLayout()
        paVLayout.addLayout(paHLayout)

        paHLayout.addWidget(QtWidgets.QLabel("First Name:"))
        self.paFirstNameEdit = QtWidgets.QLineEdit()
        self.paFirstNameEdit.setMinimumWidth(150)
        paHLayout.addWidget(self.paFirstNameEdit)

        paHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        paHLayout.addWidget(QtWidgets.QLabel("Last Name:"))
        self.paLastNameEdit = QtWidgets.QLineEdit()
        self.paLastNameEdit.setMinimumWidth(150)
        paHLayout.addWidget(self.paLastNameEdit)

        paHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        paHLayout.addWidget(QtWidgets.QLabel("Date of Birth:"))
        self.paDOBEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.paDOBEdit.setMinimumWidth(100)
        paHLayout.addWidget(self.paDOBEdit)

        paHLayout.addStretch()

        self.paModel = QtSql.QSqlQueryModel()
        self.paView = QtWidgets.QTableView()
        self.paView.setModel(self.paModel)
        paVLayout.addWidget(self.paView)

        paButtonLayout = QtWidgets.QHBoxLayout()
        paVLayout.addLayout(paButtonLayout)
        paButtonLayout.addStretch()
        self.deletePassengerButton = QtWidgets.QPushButton("Delete Account")
        self.deletePassengerButton.clicked.connect(self.deletePassenger)
        paButtonLayout.addWidget(self.deletePassengerButton)

        # Passenger bookings tab
        passengerBookingsTab = QtWidgets.QWidget()
        passengersTab.addTab(passengerBookingsTab, "Bookings")

        pbVLayout = QtWidgets.QVBoxLayout(passengerBookingsTab)
        pbHLayout = QtWidgets.QHBoxLayout()
        pbVLayout.addLayout(pbHLayout)

        pbHLayout.addWidget(QtWidgets.QLabel("From:"))
        self.pbFromDateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.pbFromDateEdit.setMinimumWidth(100)
        pbHLayout.addWidget(self.pbFromDateEdit)
        self.pbFromCheckBox = QtWidgets.QCheckBox()

        pbHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        pbHLayout.addWidget(QtWidgets.QLabel("To:"))
        self.pbToDateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addDays(14))
        self.pbToDateEdit.setMinimumWidth(100)
        pbHLayout.addWidget(self.pbToDateEdit)
        self.pbToCheckBox = QtWidgets.QCheckBox()
        pbHLayout.addWidget(self.pbToCheckBox)

        pbHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        pbHLayout.addWidget(QtWidgets.QLabel("Airline:"))
        self.pbAirlineComboBox = QtWidgets.QComboBox()
        self.pbAirlineComboBox.setMinimumWidth(150)
        pbHLayout.addWidget(self.pbAirlineComboBox)

        pbHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        pbHLayout.addWidget(QtWidgets.QLabel("Destination:"))
        self.pbDestinationLineEdit = QtWidgets.QLineEdit()
        self.pbDestinationLineEdit.setFixedWidth(70)
        pbHLayout.addWidget(self.pbDestinationLineEdit)

        pbHLayout.addStretch()

        self.pbModel = QtSql.QSqlQueryModel()
        self.pbView = QtWidgets.QTableView()
        self.pbView.setModel(self.pbModel)
        pbVLayout.addWidget(self.pbView)

        pbButtonLayout = QtWidgets.QHBoxLayout()
        pbVLayout.addLayout(pbButtonLayout)
        pbButtonLayout.addStretch()

        self.pbModifyBookingButton = QtWidgets.QPushButton("Modify Booking")
        self.pbModifyBookingButton.clicked.connect(self.modifyPassengerBooking)
        pbButtonLayout.addWidget(self.pbModifyBookingButton)

        self.pbRemoveBookingButton = QtWidgets.QPushButton("Remove Booking")
        self.pbRemoveBookingButton.clicked.connect(self.removePassengerBooking)
        pbButtonLayout.addWidget(self.pbRemoveBookingButton)

        # Crew accounts tab
        crewAccountsTab = QtWidgets.QWidget()
        crewTab.addTab(crewAccountsTab, "Accounts")

        caVLayout = QtWidgets.QVBoxLayout(crewAccountsTab)
        caHLayout = QtWidgets.QHBoxLayout()
        caVLayout.addLayout(caHLayout)

        caHLayout.addWidget(QtWidgets.QLabel("First Name:"))
        self.caFirstNameEdit = QtWidgets.QLineEdit()
        self.caFirstNameEdit.setMinimumWidth(150)
        caHLayout.addWidget(self.caFirstNameEdit)

        caHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        caHLayout.addWidget(QtWidgets.QLabel("Last Name:"))
        self.caLastNameEdit = QtWidgets.QLineEdit()
        self.caLastNameEdit.setMinimumWidth(150)
        caHLayout.addWidget(self.caLastNameEdit)

        caHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        caHLayout.addWidget(QtWidgets.QLabel("Date of Birth:"))
        self.caDOBEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.caDOBEdit.setMinimumWidth(100)
        caHLayout.addWidget(self.caDOBEdit)

        caHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        caHLayout.addWidget(QtWidgets.QLabel("Position:"))
        self.caPositionEdit = QtWidgets.QLineEdit()
        self.caPositionEdit.setMinimumWidth(150)
        caHLayout.addWidget(self.caPositionEdit)

        caHLayout.addStretch()

        self.caModel = QtSql.QSqlQueryModel()
        self.caView = QtWidgets.QTableView()
        self.caView.setModel(self.caModel)
        caVLayout.addWidget(self.caView)

        caButtonLayout = QtWidgets.QHBoxLayout()
        caVLayout.addLayout(caButtonLayout)
        caButtonLayout.addStretch()

        self.createCrewButton = QtWidgets.QPushButton("Create Account")
        self.createCrewButton.clicked.connect(self.createCrew)
        caButtonLayout.addWidget(self.createCrewButton)

        self.deleteCrewButton = QtWidgets.QPushButton("Delete Account")
        self.deleteCrewButton.clicked.connect(self.deleteCrew)
        caButtonLayout.addWidget(self.deleteCrewButton)

        # Crew bookings tab
        crewBookingsTab = QtWidgets.QWidget()
        crewTab.addTab(crewBookingsTab, "Bookings")

        cbVLayout = QtWidgets.QVBoxLayout(crewBookingsTab)
        cbHLayout = QtWidgets.QHBoxLayout()
        cbVLayout.addLayout(cbHLayout)

        cbHLayout.addWidget(QtWidgets.QLabel("From:"))
        self.cbFromDateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.cbFromDateEdit.setMinimumWidth(100)
        cbHLayout.addWidget(self.cbFromDateEdit)
        self.cbFromCheckBox = QtWidgets.QCheckBox()

        cbHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        cbHLayout.addWidget(QtWidgets.QLabel("To:"))
        self.cbToDateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addDays(14))
        self.cbToDateEdit.setMinimumWidth(100)
        cbHLayout.addWidget(self.cbToDateEdit)
        self.cbToCheckBox = QtWidgets.QCheckBox()
        cbHLayout.addWidget(self.cbToCheckBox)

        cbHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        cbHLayout.addWidget(QtWidgets.QLabel("Airline:"))
        self.cbAirlineComboBox = QtWidgets.QComboBox()
        self.cbAirlineComboBox.setMinimumWidth(150)
        cbHLayout.addWidget(self.cbAirlineComboBox)

        cbHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        cbHLayout.addWidget(QtWidgets.QLabel("Destination:"))
        self.cbDestinationLineEdit = QtWidgets.QLineEdit()
        self.cbDestinationLineEdit.setFixedWidth(70)
        cbHLayout.addWidget(self.cbDestinationLineEdit)

        cbHLayout.addStretch()

        self.cbModel = QtSql.QSqlQueryModel()
        self.cbView = QtWidgets.QTableView()
        self.cbView.setModel(self.cbModel)
        cbVLayout.addWidget(self.cbView)

        cbButtonLayout = QtWidgets.QHBoxLayout()
        cbVLayout.addLayout(cbButtonLayout)
        cbButtonLayout.addStretch()
        self.cbRemoveBookingButton = QtWidgets.QPushButton("Remove Booking")
        self.cbRemoveBookingButton.clicked.connect(self.removeCrewBooking)
        cbButtonLayout.addWidget(self.cbRemoveBookingButton)

        self.resize(1120, 590)

    @QtCore.Slot()
    def openAddFlightDialog(self) -> None:
        dialog = AddFlightDialog(False)
        dialog.exec()

    @QtCore.Slot()
    def openModifyFlightDialog(self) -> None:
        dialog = AddFlightDialog(True)
        dialog.exec()

    @QtCore.Slot()
    def removeFlight(self) -> None:
        print("Remove flight here")
    
    @QtCore.Slot()
    def deletePassenger(self) -> None:
        print("Delete passenger here")

    @QtCore.Slot()
    def openPassengerBookingDialog(self) -> None:
        dialog = AddPassengerBookingDialog()
        dialog.exec()

    @QtCore.Slot()
    def openCrewBookingDialog(self) -> None:
        dialog = AddCrewBookingDialog()
        dialog.exec()

    @QtCore.Slot()
    def modifyPassengerBooking(self) -> None:
        dialog = ModifyBookingDialog()
        dialog.exec()

    @QtCore.Slot()
    def removePassengerBooking(self) -> None:
        print("Remove booking here")

    @QtCore.Slot()
    def createCrew(self) -> None:
        dialog = CreateCrewDialog()
        dialog.exec()

    @QtCore.Slot()
    def deleteCrew(self) -> None:
        print("Delete crew here")

    @QtCore.Slot()
    def removeCrewBooking(self) -> None:
        print("Remove booking here")

class AddFlightDialog(QtWidgets.QDialog):
    def __init__(self, modifyingFlight) -> None:
        super().__init__()

        if not modifyingFlight:
            self.setWindowTitle("Airport Manager - Add Flight")
        else:
            self.setWindowTitle("Airport Manager - Modify Flight")

        self.layout = QtWidgets.QFormLayout(self)

        self.planeComboBox = QtWidgets.QComboBox()
        self.layout.addRow("Plane:", self.planeComboBox)

        self.depTermLineEdit = QtWidgets.QLineEdit()
        self.layout.addRow("Departure Terminal:", self.depTermLineEdit)

        self.depDateTimeEdit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.layout.addRow("Departure Time:", self.depDateTimeEdit)

        self.arrDateTimeEdit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.layout.addRow("Arrival Time:", self.arrDateTimeEdit)

        self.destLineEdit = QtWidgets.QLineEdit()
        self.destLineEdit.setMaxLength(3)
        self.layout.addRow("Destination Airport:", self.destLineEdit)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addRow(buttonBox)

        self.resize(380, 180)

class AddPassengerBookingDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Add Passenger Booking")

        self.layout = QtWidgets.QFormLayout(self)

        self.passengersComboBox = QtWidgets.QComboBox()
        self.layout.addRow("Passenger:", self.passengersComboBox)

        self.seatNumComboBox = QtWidgets.QComboBox()
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

class CreateCrewDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Create Crew")

        self.layout = QtWidgets.QFormLayout(self)

        self.firstNameLineEdit = QtWidgets.QLineEdit()
        self.layout.addRow("First Name:", self.firstNameLineEdit)

        self.lastNameLineEdit = QtWidgets.QLineEdit()
        self.layout.addRow("Last Name:", self.lastNameLineEdit)

        self.dobDateEdit = QtWidgets.QDateEdit()
        self.layout.addRow("Date of Birth:", self.dobDateEdit)

        self.positionEdit = QtWidgets.QLineEdit()
        self.layout.addRow("Position:", self.positionEdit)

        self.signUpUsernameLineEdit = QtWidgets.QLineEdit()
        self.layout.addRow("Username:", self.signUpUsernameLineEdit)

        self.signUpPasswordLineEdit = QtWidgets.QLineEdit()
        self.signUpPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.layout.addRow("Password:", self.signUpPasswordLineEdit)

        createAccountButton = QtWidgets.QPushButton("Create Account")
        createAccountButton.clicked.connect(self.createAccountButtonClicked)
        self.layout.addRow(createAccountButton)

    @QtCore.Slot()
    def createAccountButtonClicked(self) -> None:
        print("Create account here")
        self.accept()

class AddCrewBookingDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Add Crew Booking")

        self.layout = QtWidgets.QFormLayout(self)

        self.crewComboBox = QtWidgets.QComboBox()
        self.layout.addRow("Crew Member:", self.crewComboBox)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addRow(buttonBox)


def addPassengerToFlight(self, passenger_id, flight_id, seat_num):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO Bookings (pid, fid, seat_num) VALUES (?, ?, ?)")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    query.addBindValue(seat_num)
    if not query.exec():
        print("Error adding passenger to flight:", query.lastError().text())

def removePassengerFromFlight(self, passenger_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Bookings WHERE pid = ? AND fid = ?")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error removing passenger from flight:", query.lastError().text())

def changeSeatOnFlight(self, passenger_id, flight_id, new_seat_id):
    query = QtSql.QSqlQuery()
    query.prepare("UPDATE Bookings SET seat_num = ? WHERE pid = ? AND fid = ?")
    query.addBindValue(new_seat_id)
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error changing seat:", query.lastError().text())

def addBag(self, passenger_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO Bags (pid, fid) VALUES (?, ?)")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error adding bag:", query.lastError().text())

def removeBag(self, bag_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Bags WHERE bid = ?")
    query.addBindValue(bag_id)
    if not query.exec():
        print("Error removing bag:", query.lastError().text())

def viewCrewSchedules(self):
    query = QtSql.QSqlQuery()
    query.prepare("""SELECT c.fname, c.lname, c.cid, p.model_name, s.dep_term, s.dep_time, s.arr_term, s.arr_time, s.dest_airport
                     FROM Crew c, CrewBookings cb, Schedule s, Plane p
                     WHERE c.cid = cb.cid AND cb.fid = s.fid AND s.plane_id = p.plane_id""")
    if not query.exec():
        print("Error viewing crew schedules:", query.lastError().text())
    else:
        # NEED TO FIGURE OUT HOW TO DISPLAY
        self.crewSchedulesModel.setQuery(query)

def addNewCrewMember(self, first_name, last_name, date_of_birth, role):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO Crew (fname, lname, dob, position) VALUES (?, ?, ?, ?)")
    query.addBindValue(first_name)
    query.addBindValue(last_name)
    query.addBindValue(date_of_birth)
    query.addBindValue(role)
    if not query.exec():
        print("Error adding new crew member:", query.lastError().text())

def modifyCrewSchedule(self, crew_id, flight_id, add=True):
    query = QtSql.QSqlQuery()
    if add:
        query.prepare("INSERT INTO CrewBookings (cid, fid) VALUES (?, ?)")
    else:
        query.prepare("DELETE FROM CrewBookings WHERE cid = ? AND fid = ?")
    query.addBindValue(crew_id)
    query.addBindValue(flight_id)
    if not query.exec():
        action = "adding" if add else "removing"
        print(f"Error {action} crew member's schedule:", query.lastError().text())

def modifyFlight(self, plane_id, dep_term, dep_time, arr_term, arr_time, dest_airport, flight_id=None):
    query = QtSql.QSqlQuery()
    if flight_id:  # Modify existing flight
        query.prepare("UPDATE Schedule SET plane_id = ?, dep_term = ?, dep_time = ?, arr_term = ?, arr_time = ?, dest_airport = ? WHERE fid = ?")
        query.addBindValue(plane_id)
        query.addBindValue(dep_term)
        query.addBindValue(dep_time)
        query.addBindValue(arr_term)
        query.addBindValue(arr_time)
        query.addBindValue(dest_airport)
        query.addBindValue(flight_id)
    else:  # Add new flight
        query.prepare("INSERT INTO Schedule (plane_id, dep_term, dep_time, arr_term, arr_time, dest_airport) VALUES (?, ?, ?, ?, ?, ?)")
        query.addBindValue(plane_id)
        query.addBindValue(dep_term)
        query.addBindValue(dep_time)
        query.addBindValue(arr_term)
        query.addBindValue(arr_time)
        query.addBindValue(dest_airport)
    if not query.exec():
        action = "modifying" if flight_id else "adding"
        print(f"Error {action} flight:", query.lastError().text())

def getPassengersByAirlineAndDate(self, airline_name, date):
    query = QtSql.QSqlQuery()
    query.prepare("""SELECT fname, lname, pid
                     FROM Passengers NATURAL JOIN Bookings NATURAL JOIN Schedule NATURAL JOIN Planes NATURAL JOIN Airlines a
                     WHERE a.name = ? AND CAST(dep_time AS DATE) = ?""")
    query.addBindValue(airline_name)
    query.addBindValue(date)
    if not query.exec():
        print("Error retrieving passengers:", query.lastError().text())
    else:
        # NEED TO FIGURE OUT HOW TO DISPLAY
        self.passengersModel.setQuery(query)
