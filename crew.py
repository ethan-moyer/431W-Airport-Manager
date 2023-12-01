from PySide6 import QtCore, QtWidgets, QtSql

class CrewWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager")

        tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(tabWidget)

        flightsTab = QtWidgets.QWidget()
        tabWidget.addTab(flightsTab, "Flights")

        scheduleTab = QtWidgets.QWidget()
        tabWidget.addTab(scheduleTab, "Work Schedule")

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

        self.scheduleFlightsButton = QtWidgets.QPushButton("Add Flight To Schedule")
        self.scheduleFlightsButton.clicked.connect(self.scheduleFlight)
        flightsButtonLayout.addWidget(self.scheduleFlightsButton)

        # Work schedule tab
        scheduleVLayout = QtWidgets.QVBoxLayout(scheduleTab)

        self.scheduleModel = QtSql.QSqlQueryModel()
        self.scheduleView = QtWidgets.QTableView()
        self.scheduleView.setModel(self.scheduleModel)
        scheduleVLayout.addWidget(self.scheduleView)

        scheduleButtonLayout = QtWidgets.QHBoxLayout()
        scheduleVLayout.addLayout(scheduleButtonLayout)
        scheduleButtonLayout.addStretch()

        self.scheduleDetailsButton = QtWidgets.QPushButton("View Details")
        self.scheduleDetailsButton.clicked.connect(self.openDetailsDialog)
        scheduleButtonLayout.addWidget(self.scheduleDetailsButton)

        self.removeScheduleButton = QtWidgets.QPushButton("Remove Flight From Schedule")
        self.removeScheduleButton.clicked.connect(self.removeFromSchedule)
        scheduleButtonLayout.addWidget(self.removeScheduleButton)

        self.resize(1120, 590)

    @QtCore.Slot()
    def scheduleFlight(self) -> None:
        print("Schedule flight here")

    @QtCore.Slot()
    def openDetailsDialog(self) -> None:
        details = FlightDetailsDialog()
        details.exec()

    @QtCore.Slot()
    def removeFromSchedule(self) -> None:
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

        self.layout.addStretch()

        self.layout.addWidget(QtWidgets.QLabel("Crew:"))
        crewModel = QtSql.QSqlQueryModel()
        crewView = QtWidgets.QTableView()
        crewView.setModel(crewModel)
        self.layout.addWidget(crewView)

        self.resize(450, 630)


def viewWorkSchedule(self, crew_id):
    query = QtSql.QSqlQuery()
    query.prepare("""SELECT p.model_name, s.dep_term, s.dep_time, s.arr_term, s.arr_time, s.dest_airport
                     FROM CrewBookings c, Planes p, Schedule s
                     WHERE c.fid = s.fid AND s.plane_id = p.plane_id AND c.cid = ?""")
    query.addBindValue(crew_id)
    if not query.exec():
        print("Error viewing work schedule:", query.lastError().text())
    else:
        self.scheduleModel.setQuery(query)

def addToFlightSchedule(self, crew_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO CrewBookings (cid, fid) VALUES (?, ?)")
    query.addBindValue(crew_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error adding to flight schedule:", query.lastError().text())

def removeFromFlightSchedule(self, crew_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM CrewBookings WHERE cid = ? AND fid = ?")
    query.addBindValue(crew_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error removing from flight schedule:", query.lastError().text())

def viewFlightDetails(self, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("""SELECT NULL AS seat_num, fname as first_name, lname as last_name
                     FROM Crew WHERE cid IN 
                     (SELECT cid FROM CrewBookings WHERE fid = ?)
                     UNION ALL
                     SELECT seat_num as seat_num, fname as first_name, lname as last_name
                     FROM Passengers WHERE pid IN 
                     (SELECT pid FROM Bookings WHERE fid = ?) 
                     ORDER BY case when seat_num IS NULL then 0 else 1 end, seat_num;""")
    query.addBindValue(flight_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error viewing flight details:", query.lastError().text())
    else:
        self.detailsModel.setQuery(query)
