from PySide6 import QtCore, QtWidgets, QtSql

class CrewWindow(QtWidgets.QMainWindow):
    def __init__(self, crew_id) -> None:
        super().__init__()
        self.crew_id = crew_id

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
        self.flightsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.flightsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
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
        self.scheduleView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.scheduleView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
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

        self.updateFlightsView()
        self.updateScheduleView()

    def updateFlightsView(self):
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM Schedule")  # Adjust this query based on your database schema
        query.exec_()
        self.flightsModel.setQuery(query)

    def updateScheduleView(self):
        # Fetch and display crew's scheduled flights
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM CrewBookings WHERE cid = :cid")  # Adjust as needed
        query.bindValue(":cid", self.crew_id)
        query.exec_()
        self.scheduleModel.setQuery(query)

    @QtCore.Slot()
    def scheduleFlight(self) -> None:
        # print("Schedule flight here")
        selectedFlightIndex = self.flightsView.currentIndex()
        if selectedFlightIndex.isValid():
            flight_id = self.flightsModel.record(selectedFlightIndex.row()).value("fid")
            addToFlightSchedule(self, self.crew_id, flight_id)
            self.updateScheduleView()
            self.updateFlightsView()
            
    @QtCore.Slot()
    def openDetailsDialog(self) -> None:
        selectedFlightIndex = self.flightsView.currentIndex()
        if selectedFlightIndex.isValid():
            flight_id = self.flightsModel.record(selectedFlightIndex.row()).value("fid")
            details = FlightDetailsDialog(flight_id)
            details.exec()

    @QtCore.Slot()
    def removeFromSchedule(self) -> None:
        # print("Remove flight here")
        selectedFlightIndex = self.scheduleView.currentIndex()
        if selectedFlightIndex.isValid():
            flight_id = self.scheduleModel.record(selectedFlightIndex.row()).value("fid")
            removeFromFlightSchedule(self, self.crew_id, flight_id)
            self.updateScheduleView()
            self.updateFlightsView()

class FlightDetailsDialog(QtWidgets.QDialog):
    def __init__(self, flight_id) -> None:
        super().__init__()
        self.flight_id = flight_id

        self.setWindowTitle("Airport Manager - Flight Details")

        self.layout = QtWidgets.QVBoxLayout(self)
        
        # Flight Details Labels
        self.flightIDLabel = QtWidgets.QLabel("Flight ID: ")
        self.airlineLabel = QtWidgets.QLabel("Airline: ")
        self.planeLabel = QtWidgets.QLabel("Plane: ")
        self.departureTermLabel = QtWidgets.QLabel("Departure Terminal: ")
        self.departureTimeLabel = QtWidgets.QLabel("Departure Time: ")
        self.arrivalTermLabel = QtWidgets.QLabel("Arrival Terminal: ")
        self.arrivalTimeLabel = QtWidgets.QLabel("Arrival Time: ")
        self.destinationLabel = QtWidgets.QLabel("Destination: ")

        self.layout.addWidget(self.flightIDLabel)
        self.layout.addWidget(self.airlineLabel)
        self.layout.addWidget(self.planeLabel)
        self.layout.addWidget(self.departureTermLabel)
        self.layout.addWidget(self.departureTimeLabel)
        self.layout.addWidget(self.arrivalTermLabel)
        self.layout.addWidget(self.arrivalTimeLabel)
        self.layout.addWidget(self.destinationLabel)
        
        self.layout.addStretch()

        self.layout.addWidget(QtWidgets.QLabel("Passengers:"))
        self.passengersModel = QtSql.QSqlQueryModel()
        self.passengersView = QtWidgets.QTableView()
        self.passengersView.setModel(self.passengersModel)
        self.passengersView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.passengersView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
        self.layout.addWidget(self.passengersView)

        self.layout.addStretch()

        self.layout.addWidget(QtWidgets.QLabel("Crew:"))
        self.crewModel = QtSql.QSqlQueryModel()
        self.crewView = QtWidgets.QTableView()
        self.crewView.setModel(self.crewModel)
        self.crewView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.crewView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
        self.layout.addWidget(self.crewView)

        self.resize(450, 630)
        viewFlightDetails(self, flight_id)

        self.populateFlightDetails()

    def populateFlightDetails(self):
        # Fetch and display general flight details
        self.populateGeneralFlightInfo()

        # Populate passengers and crew information
        self.populatePassengers()
        self.populateCrew()

    def populateGeneralFlightInfo(self):
        query = QtSql.QSqlQuery()
        query.prepare("""
            SELECT S.fid, A.name AS airline, P.model_name, S.dep_term, S.dep_time, S.arr_term, S.arr_time, S.dest_airport
            FROM Schedule S
            JOIN Planes P ON S.plane_id = P.plane_id
            JOIN Airlines A ON P.aid = A.aid
            WHERE S.fid = :flight_id
        """)
        query.bindValue(":flight_id", self.flight_id)
        if query.exec_() and query.next():
            self.flightIDLabel.setText(f"Flight ID: {query.value(0)}")
            self.airlineLabel.setText(f"Airline: {query.value(1)}")
            self.planeLabel.setText(f"Plane: {query.value(2)}")
            self.departureTermLabel.setText(f"Departure Terminal: {query.value(3)}")
            self.departureTimeLabel.setText(f"Departure Time: {query.value(4)}")
            self.arrivalTermLabel.setText(f"Arrival Terminal: {query.value(5)}")
            self.arrivalTimeLabel.setText(f"Arrival Time: {query.value(6)}")
            self.destinationLabel.setText(f"Destination: {query.value(7)}")
        else:
            print("Error fetching general flight details:", query.lastError().text())

    def populatePassengers(self):
        query = QtSql.QSqlQuery()
        query.prepare("""
            SELECT P.pid, P.fname || ' ' || P.lname AS name, B.seat_num 
            FROM Passengers P 
            JOIN Bookings B ON P.pid = B.pid 
            WHERE B.fid = :flight_id
        """)
        query.bindValue(":flight_id", self.flight_id)
        query.exec_()
        self.passengersModel.setQuery(query)

    def populateCrew(self):
        query = QtSql.QSqlQuery()
        query.prepare("""
            SELECT C.cid, C.fname || ' ' || C.lname AS name, C.position 
            FROM Crew C 
            JOIN CrewBookings CB ON C.cid = CB.cid 
            WHERE CB.fid = :flight_id
        """)
        query.bindValue(":flight_id", self.flight_id)
        query.exec_()
        self.crewModel.setQuery(query)

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
    if not query.exec_():
        print("Error adding to flight schedule:", query.lastError().text())


def removeFromFlightSchedule(self, crew_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM CrewBookings WHERE cid = ? AND fid = ?")
    query.addBindValue(crew_id)
    query.addBindValue(flight_id)
    if not query.exec_():
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
