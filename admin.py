from PySide6 import QtCore, QtWidgets, QtSql
from passenger import ModifyBookingDialog, changeSeat, removeBooking, getAvailableSeats, addBooking

class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager")

        tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(tabWidget)

        flightsTab = QtWidgets.QWidget()
        tabWidget.addTab(flightsTab, "Flights")

        self.passengersTab = QtWidgets.QTabWidget()
        tabWidget.addTab(self.passengersTab, "Passengers")

        self.crewTab = QtWidgets.QTabWidget()
        tabWidget.addTab(self.crewTab, "Crew")

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
        self.destinationLineEdit.setMaxLength(3)
        self.destinationLineEdit.setFixedWidth(70)
        flightsHLayout.addWidget(self.destinationLineEdit)

        flightsHLayout.addStretch()

        self.flightsModel = QtSql.QSqlQueryModel()
        self.flightsView = QtWidgets.QTableView()
        self.flightsView.setModel(self.flightsModel)
        # Select rows instead of cells
        self.flightsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.flightsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.flightsView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
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
        self.passengersTab.addTab(passengerAccountsTab, "Accounts")

        paVLayout = QtWidgets.QVBoxLayout(passengerAccountsTab)
        paHLayout = QtWidgets.QHBoxLayout()
        paVLayout.addLayout(paHLayout)

        paHLayout.addWidget(QtWidgets.QLabel("First Name:"))
        self.paFirstNameEdit = QtWidgets.QLineEdit()
        self.paFirstNameEdit.setMaxLength(31)
        self.paFirstNameEdit.setMinimumWidth(150)
        paHLayout.addWidget(self.paFirstNameEdit)

        paHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        paHLayout.addWidget(QtWidgets.QLabel("Last Name:"))
        self.paLastNameEdit = QtWidgets.QLineEdit()
        self.paLastNameEdit.setMaxLength(31)
        self.paLastNameEdit.setMinimumWidth(150)
        paHLayout.addWidget(self.paLastNameEdit)

        paHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        paHLayout.addWidget(QtWidgets.QLabel("Date of Birth:"))
        self.paDOBEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.paDOBEdit.setMinimumWidth(100)
        paHLayout.addWidget(self.paDOBEdit)
        self.paDOBCheckBox = QtWidgets.QCheckBox("Use DOB Filter")
        paHLayout.addWidget(self.paDOBCheckBox)
        
        paHLayout.addStretch()

        self.paModel = QtSql.QSqlQueryModel()
        self.paView = QtWidgets.QTableView()
        self.paView.setModel(self.paModel)
        # Select rows instead of cells
        self.paView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.paView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.paView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        paVLayout.addWidget(self.paView)

        paButtonLayout = QtWidgets.QHBoxLayout()
        paVLayout.addLayout(paButtonLayout)
        paButtonLayout.addStretch()
        self.deletePassengerButton = QtWidgets.QPushButton("Delete Account")
        self.deletePassengerButton.clicked.connect(self.deletePassenger)
        paButtonLayout.addWidget(self.deletePassengerButton)

        # Passenger bookings tab
        passengerBookingsTab = QtWidgets.QWidget()
        self.passengersTab.addTab(passengerBookingsTab, "Bookings")

        pbVLayout = QtWidgets.QVBoxLayout(passengerBookingsTab)
        pbHLayout = QtWidgets.QHBoxLayout()
        pbVLayout.addLayout(pbHLayout)

        pbHLayout.addWidget(QtWidgets.QLabel("From:"))
        self.pbFromDateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.pbFromDateEdit.setMinimumWidth(100)
        pbHLayout.addWidget(self.pbFromDateEdit)
        self.pbFromCheckBox = QtWidgets.QCheckBox()
        pbHLayout.addWidget(self.pbFromCheckBox)

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
        self.pbDestinationLineEdit.setMaxLength(3)
        self.pbDestinationLineEdit.setFixedWidth(70)
        pbHLayout.addWidget(self.pbDestinationLineEdit)

        pbHLayout.addStretch()

        self.pbModel = QtSql.QSqlQueryModel()
        self.pbView = QtWidgets.QTableView()
        self.pbView.setModel(self.pbModel)
        # Select rows instead of cells
        self.pbView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.pbView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.pbView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
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
        self.crewTab.addTab(crewAccountsTab, "Accounts")

        caVLayout = QtWidgets.QVBoxLayout(crewAccountsTab)
        caHLayout = QtWidgets.QHBoxLayout()
        caVLayout.addLayout(caHLayout)

        caHLayout.addWidget(QtWidgets.QLabel("First Name:"))
        self.caFirstNameEdit = QtWidgets.QLineEdit()
        self.caFirstNameEdit.setMaxLength(31)
        self.caFirstNameEdit.setMinimumWidth(150)
        caHLayout.addWidget(self.caFirstNameEdit)

        caHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        caHLayout.addWidget(QtWidgets.QLabel("Last Name:"))
        self.caLastNameEdit = QtWidgets.QLineEdit()
        self.caLastNameEdit.setMaxLength(31)
        self.caLastNameEdit.setMinimumWidth(150)
        caHLayout.addWidget(self.caLastNameEdit)

        caHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        caHLayout.addWidget(QtWidgets.QLabel("Date of Birth:"))
        self.caDOBEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.caDOBEdit.setMinimumWidth(100)
        caHLayout.addWidget(self.caDOBEdit)
        self.caDOBCheckBox = QtWidgets.QCheckBox("Use DOB Filter")
        caHLayout.addWidget(self.caDOBCheckBox)

        caHLayout.addSpacerItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred))

        caHLayout.addWidget(QtWidgets.QLabel("Position:"))
        self.caPositionEdit = QtWidgets.QLineEdit()
        self.caPositionEdit.setMaxLength(31)
        self.caPositionEdit.setMinimumWidth(150)
        caHLayout.addWidget(self.caPositionEdit)

        caHLayout.addStretch()

        self.caModel = QtSql.QSqlQueryModel()
        self.caView = QtWidgets.QTableView()
        self.caView.setModel(self.caModel)
        # Select rows instead of cells
        self.caView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.caView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.caView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
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
        self.crewTab.addTab(crewBookingsTab, "Bookings")

        cbVLayout = QtWidgets.QVBoxLayout(crewBookingsTab)
        cbHLayout = QtWidgets.QHBoxLayout()
        cbVLayout.addLayout(cbHLayout)

        cbHLayout.addWidget(QtWidgets.QLabel("From:"))
        self.cbFromDateEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.cbFromDateEdit.setMinimumWidth(100)
        cbHLayout.addWidget(self.cbFromDateEdit)
        self.cbFromCheckBox = QtWidgets.QCheckBox()
        cbHLayout.addWidget(self.cbFromCheckBox)

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
        self.cbDestinationLineEdit.setMaxLength(3)
        self.cbDestinationLineEdit.setFixedWidth(70)
        cbHLayout.addWidget(self.cbDestinationLineEdit)

        cbHLayout.addStretch()

        self.cbModel = QtSql.QSqlQueryModel()
        self.cbView = QtWidgets.QTableView()
        self.cbView.setModel(self.cbModel)
        # Select rows instead of cells
        self.cbView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.cbView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.cbView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        cbVLayout.addWidget(self.cbView)

        cbButtonLayout = QtWidgets.QHBoxLayout()
        cbVLayout.addLayout(cbButtonLayout)
        cbButtonLayout.addStretch()
        self.cbRemoveBookingButton = QtWidgets.QPushButton("Remove Booking")
        self.cbRemoveBookingButton.clicked.connect(self.removeCrewBooking)
        cbButtonLayout.addWidget(self.cbRemoveBookingButton)

        self.populateAirlineComboBoxes()

        # LINK EDITS TO UPDATES
        self.fromDateEdit.dateChanged.connect(self.populateFlightsModel)
        self.toDateEdit.dateChanged.connect(self.populateFlightsModel)
        self.airlineComboBox.currentIndexChanged.connect(self.populateFlightsModel)
        self.destinationLineEdit.textChanged.connect(self.populateFlightsModel)
        self.fromCheckBox.stateChanged.connect(self.populateFlightsModel)
        self.toCheckBox.stateChanged.connect(self.populateFlightsModel)

        self.pbFromDateEdit.dateChanged.connect(self.populatePBModel)
        self.pbToDateEdit.dateChanged.connect(self.populatePBModel)
        self.pbAirlineComboBox.currentIndexChanged.connect(self.populatePBModel)
        self.pbDestinationLineEdit.textChanged.connect(self.populatePBModel)
        self.pbFromCheckBox.stateChanged.connect(self.populatePBModel)
        self.pbToCheckBox.stateChanged.connect(self.populatePBModel)

        self.cbFromDateEdit.dateChanged.connect(self.populateCBModel)
        self.cbToDateEdit.dateChanged.connect(self.populateCBModel)
        self.cbAirlineComboBox.currentIndexChanged.connect(self.populateCBModel)
        self.cbDestinationLineEdit.textChanged.connect(self.populateCBModel)
        self.cbFromCheckBox.stateChanged.connect(self.populateCBModel)
        self.cbToCheckBox.stateChanged.connect(self.populateCBModel)

        self.paDOBCheckBox.stateChanged.connect(self.populatePAModel)
        self.paFirstNameEdit.textChanged.connect(self.populatePAModel)
        self.paLastNameEdit.textChanged.connect(self.populatePAModel)
        self.paDOBEdit.dateChanged.connect(self.populatePAModel)

        self.caDOBCheckBox.stateChanged.connect(self.populateCAModel)
        self.caFirstNameEdit.textChanged.connect(self.populateCAModel)
        self.caLastNameEdit.textChanged.connect(self.populateCAModel)
        self.caPositionEdit.textChanged.connect(self.populateCAModel)
        self.caDOBEdit.dateChanged.connect(self.populateCAModel)

        self.populateFlightsModel()
        self.populatePBModel()
        self.populatePAModel()
        self.populateCBModel()
        self.populateCAModel()

        #tabWidget.currentChanged.connect(self.onTabChanged)
        #self.passengersTab.currentChanged.connect(self.onPassengerTabChanged)
        #self.crewTab.currentChanged.connect(self.onCrewTabChanged)

        #self.populateFlightsModel()

        self.resize(1120, 590)

    def onTabChanged(self, index):
        if index == 0:
            self.populateFlightsModel()
        elif index == 1:
            self.onPassengerTabChanged(self.passengersTab.currentIndex())
        else:
            self.onCrewTabChanged(self.crewTab.currentIndex())

    def onPassengerTabChanged(self, index):
        if index == 0:
            self.populatePAModel()
        else:
            self.populatePBModel()
    
    def onCrewTabChanged(self, index):
        if index == 0:
            self.populateCAModel()
        else:
            self.populateCBModel()
    
    def populateFlightsModel(self):
        # query = QtSql.QSqlQuery()
        # queryStr = "SELECT s.fid, s.dep_term, s.dep_time, s.arr_term, s.arr_time, s.dest_airport, p.model_name, a.name " \
        #         "FROM Schedule s " \
        #         "JOIN Planes p ON s.plane_id = p.plane_id " \
        #         "JOIN Airlines a ON p.aid = a.aid " \
        #         "WHERE (:fromDate IS NULL OR s.dep_time >= :fromDate) " \
        #         "AND (:toDate IS NULL OR s.dep_time <= :toDate) " \
        #         "AND (:airline IS NULL OR a.name = :airline) " \
        #         "AND (:destination IS NULL OR s.dest_airport LIKE :destination)"
        # query.prepare(queryStr)

        # fromDate = self.fromDateEdit.date().toString("yyyy-MM-dd") if self.fromCheckBox.isChecked() else None
        # toDate = self.toDateEdit.date().toString("yyyy-MM-dd") if self.toCheckBox.isChecked() else None
        # airline = self.airlineComboBox.currentText() if self.airlineComboBox.currentIndex() != 0 else None
        # destination = "%" + self.destinationLineEdit.text().strip() + "%" if self.destinationLineEdit.text() else None

        # query.bindValue(":fromDate", fromDate)
        # query.bindValue(":toDate", toDate)
        # query.bindValue(":airline", airline)
        # query.bindValue(":destination", destination)

        # if not query.exec_():
        #     print("Error retrieving flights:", query.lastError().text())
        # else:
        #     self.flightsModel.setQuery(query)

        query = QtSql.QSqlQuery()
        queryStr = "SELECT s.fid, s.dep_term, s.dep_time, s.arr_term, s.arr_time, s.dest_airport, p.plane_id, p.model_name, a.name " \
                "FROM Schedule s " \
                "JOIN Planes p ON s.plane_id = p.plane_id " \
                "JOIN Airlines a ON p.aid = a.aid WHERE 1=1"
        
        binding = {}
        
        if self.fromCheckBox.isChecked():
            fromDate = self.fromDateEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND s.dep_time >= :fromDate"
            # query.bindValue(":fromDate", fromDate)
            binding[':fromDate'] = fromDate

        if self.toCheckBox.isChecked():
            toDate = self.toDateEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND s.dep_time <= :toDate"
            # query.bindValue(":toDate", toDate)
            binding[":toDate"] = toDate

        if self.airlineComboBox.currentIndex() != 0:
            airline = self.airlineComboBox.currentText()
            queryStr += " AND a.name = :airline"
            # query.bindValue(":airline", airline.strip())
            binding[":airline"] = airline

        if self.destinationLineEdit.text():
            destination = "%" + self.destinationLineEdit.text().strip() + "%"
            queryStr += " AND s.dest_airport ILIKE :destination"
            # query.bindValue(":destination", destination)
            binding[":destination"] = destination
            
        query.prepare(queryStr)
        for name, value in binding.items():
            query.bindValue(name, value)

        if not query.exec_():
            QtWidgets.QMessageBox.warning(self, "Retrieving Flights Error", f"Error retrieving flights: {query.lastError().text()}")
        else:
            # print(f"Running: {query.lastQuery()}\n")
            self.flightsModel.setQuery(query)
            if self.flightsModel.lastError().isValid():
                QtWidgets.QMessageBox.warning(self, "Model Error", f"Model error: {self.flightsModel.lastError().text()}")

        # Update the model column names
        self.flightsModel.setHeaderData(0, QtCore.Qt.Horizontal, "Flight ID")
        self.flightsModel.setHeaderData(1, QtCore.Qt.Horizontal, "Dep. Terminal")
        self.flightsModel.setHeaderData(2, QtCore.Qt.Horizontal, "Dep. Time")
        self.flightsModel.setHeaderData(3, QtCore.Qt.Horizontal, "Arr. Terminal")
        self.flightsModel.setHeaderData(4, QtCore.Qt.Horizontal, "Arr. Time")
        self.flightsModel.setHeaderData(5, QtCore.Qt.Horizontal, "Dest. Airport")
        self.flightsModel.setHeaderData(6, QtCore.Qt.Horizontal, "Plane ID")
        self.flightsModel.setHeaderData(7, QtCore.Qt.Horizontal, "Model")
        self.flightsModel.setHeaderData(8, QtCore.Qt.Horizontal, "Airline")

    def populatePBModel(self):
        # query = QtSql.QSqlQuery()
        # queryStr = "SELECT b.pid, b.fid, b.seat_num, p.fname, p.lname, s.dep_time, s.arr_time, s.dest_airport " \
        #         "FROM Bookings b " \
        #         "JOIN Passengers p ON b.pid = p.pid " \
        #         "JOIN Schedule s ON b.fid = s.fid " \
        #         "WHERE (:fromDate IS NULL OR s.dep_time >= :fromDate) " \
        #         "AND (:toDate IS NULL OR s.dep_time <= :toDate) " \
        #         "AND (:airline IS NULL OR EXISTS (SELECT 1 FROM Planes pl JOIN Airlines a ON pl.aid = a.aid WHERE pl.plane_id = s.plane_id AND a.name = :airline)) " \
        #         "AND (:destination IS NULL OR s.dest_airport LIKE :destination)"
        # query.prepare(queryStr)

        # fromDate = self.pbFromDateEdit.date().toString("yyyy-MM-dd") if self.pbFromCheckBox.isChecked() else None
        # toDate = self.pbToDateEdit.date().toString("yyyy-MM-dd") if self.pbToCheckBox.isChecked() else None
        # airline = self.pbAirlineComboBox.currentText() if self.pbAirlineComboBox.currentIndex() != 0 else None
        # destination = "%" + self.pbDestinationLineEdit.text().strip() + "%" if self.pbDestinationLineEdit.text() else None

        # query.bindValue(":fromDate", fromDate)
        # query.bindValue(":toDate", toDate)
        # query.bindValue(":airline", airline)
        # query.bindValue(":destination", destination)

        # if not query.exec_():
        #     print("Error retrieving passenger bookings:", query.lastError().text())
        # else:
        #     self.pbModel.setQuery(query)
        query = QtSql.QSqlQuery()
        # queryStr = "SELECT b.pid, b.fid, b.seat_num, p.fname, p.lname, s.dep_time, s.arr_time, s.dest_airport " \
        #         "FROM Bookings b " \
        #         "JOIN Passengers p ON b.pid = p.pid " \
        #         "JOIN Schedule s ON b.fid = s.fid WHERE 1=1"
        queryStr = """SELECT b.pid, b.fid, b.seat_num, p.fname, p.lname, s.dep_time, s.arr_time, s.dest_airport,
                    (SELECT COUNT(*) FROM Bags WHERE Bags.pid = b.pid AND Bags.fid = b.fid) AS num_bags
                    FROM Bookings b 
                    JOIN Passengers p ON b.pid = p.pid 
                    JOIN Schedule s ON b.fid = s.fid WHERE 1=1
                    """

        binding = {}

        if self.pbFromCheckBox.isChecked():
            fromDate = self.pbFromDateEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND s.dep_time >= :fromDate"
            binding[':fromDate'] = fromDate

        if self.pbToCheckBox.isChecked():
            toDate = self.pbToDateEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND s.dep_time <= :toDate"
            binding[":toDate"] = toDate

        if self.pbAirlineComboBox.currentIndex() != 0:
            airline = self.pbAirlineComboBox.currentText()
            queryStr += " AND EXISTS (SELECT 1 FROM Planes pl JOIN Airlines a ON pl.aid = a.aid WHERE pl.plane_id = s.plane_id AND a.name = :airline)"
            binding[":airline"] = airline

        if self.pbDestinationLineEdit.text():
            destination = "%" + self.pbDestinationLineEdit.text().strip() + "%"
            queryStr += " AND s.dest_airport ILIKE :destination"
            binding[":destination"] = destination

        query.prepare(queryStr)
        for name, value in binding.items():
            query.bindValue(name, value)

        if not query.exec_():
            QtWidgets.QMessageBox.warning(self, "Passenger Booking Error", f"Error retrieving passenger bookings: {query.lastError().text()}")
        else:
            self.pbModel.setQuery(query)
            if self.pbModel.lastError().isValid():
                QtWidgets.QMessageBox.warning(self, "Model Error", f"Model error: {self.pbModel.lastError().text()}")

        # Update the model column names
        self.pbModel.setHeaderData(0, QtCore.Qt.Horizontal, "Passenger ID")
        self.pbModel.setHeaderData(1, QtCore.Qt.Horizontal, "Flight ID")
        self.pbModel.setHeaderData(2, QtCore.Qt.Horizontal, "Seat Num")
        self.pbModel.setHeaderData(3, QtCore.Qt.Horizontal, "First Name")
        self.pbModel.setHeaderData(4, QtCore.Qt.Horizontal, "Last Name")
        self.pbModel.setHeaderData(5, QtCore.Qt.Horizontal, "Dep. Time")
        self.pbModel.setHeaderData(6, QtCore.Qt.Horizontal, "Arr. Time")
        self.pbModel.setHeaderData(7, QtCore.Qt.Horizontal, "Dest. Airport")
        self.pbModel.setHeaderData(8, QtCore.Qt.Horizontal, "Num Bags")

    def populateCBModel(self):
        # query = QtSql.QSqlQuery()
        # queryStr = "SELECT cb.cid, cb.fid, c.fname, c.lname, c.position, s.dep_time, s.arr_time, s.dest_airport " \
        #         "FROM CrewBookings cb " \
        #         "JOIN Crew c ON cb.cid = c.cid " \
        #         "JOIN Schedule s ON cb.fid = s.fid " \
        #         "WHERE (:fromDate IS NULL OR s.dep_time >= :fromDate) " \
        #         "AND (:toDate IS NULL OR s.dep_time <= :toDate) " \
        #         "AND (:airline IS NULL OR EXISTS (SELECT 1 FROM Planes pl JOIN Airlines a ON pl.aid = a.aid WHERE pl.plane_id = s.plane_id AND a.name = :airline)) " \
        #         "AND (:destination IS NULL OR s.dest_airport LIKE :destination)"
        # query.prepare(queryStr)

        # fromDate = self.cbFromDateEdit.date().toString("yyyy-MM-dd") if self.cbFromCheckBox.isChecked() else None
        # toDate = self.cbToDateEdit.date().toString("yyyy-MM-dd") if self.cbToCheckBox.isChecked() else None
        # airline = self.cbAirlineComboBox.currentText() if self.cbAirlineComboBox.currentIndex() != 0 else None
        # destination = "%" + self.cbDestinationLineEdit.text().strip() + "%" if self.cbDestinationLineEdit.text() else None

        # query.bindValue(":fromDate", fromDate)
        # query.bindValue(":toDate", toDate)
        # query.bindValue(":airline", airline)
        # query.bindValue(":destination", destination)

        # if not query.exec_():
        #     print("Error retrieving crew bookings:", query.lastError().text())
        # else:
        #     self.cbModel.setQuery(query)
        query = QtSql.QSqlQuery()
        queryStr = "SELECT cb.cid, cb.fid, c.fname, c.lname, c.position, s.dep_time, s.arr_time, s.dest_airport " \
                "FROM CrewBookings cb " \
                "JOIN Crew c ON cb.cid = c.cid " \
                "JOIN Schedule s ON cb.fid = s.fid WHERE 1=1"

        binding = {}

        if self.cbFromCheckBox.isChecked():
            fromDate = self.cbFromDateEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND s.dep_time >= :fromDate"
            binding[':fromDate'] = fromDate

        if self.cbToCheckBox.isChecked():
            toDate = self.cbToDateEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND s.dep_time <= :toDate"
            binding[":toDate"] = toDate

        if self.cbAirlineComboBox.currentIndex() != 0:
            airline = self.cbAirlineComboBox.currentText()
            queryStr += " AND EXISTS (SELECT 1 FROM Planes pl JOIN Airlines a ON pl.aid = a.aid WHERE pl.plane_id = s.plane_id AND a.name = :airline)"
            binding[":airline"] = airline

        if self.cbDestinationLineEdit.text():
            destination = "%" + self.cbDestinationLineEdit.text().strip() + "%"
            queryStr += " AND s.dest_airport ILIKE :destination"
            binding[":destination"] = destination

        query.prepare(queryStr)
        for name, value in binding.items():
            query.bindValue(name, value)

        if not query.exec_():
            QtWidgets.QMessageBox.warning(self, "Retrieving Crew Bookings Error", f"Error retrieving crew bookings: {query.lastError().text()}")
        else:
            self.cbModel.setQuery(query)
            if self.cbModel.lastError().isValid():
                QtWidgets.QMessageBox.warning(self, "Model Error", f"Model error: {self.cbModel.lastError().text()}")

        # Update the model column names
        self.cbModel.setHeaderData(0, QtCore.Qt.Horizontal, "Crew ID")
        self.cbModel.setHeaderData(1, QtCore.Qt.Horizontal, "Flight ID")
        self.cbModel.setHeaderData(2, QtCore.Qt.Horizontal, "First Name")
        self.cbModel.setHeaderData(3, QtCore.Qt.Horizontal, "Last Name")
        self.cbModel.setHeaderData(4, QtCore.Qt.Horizontal, "Position")
        self.cbModel.setHeaderData(5, QtCore.Qt.Horizontal, "Dep. Time")
        self.cbModel.setHeaderData(6, QtCore.Qt.Horizontal, "Arr. Time")
        self.cbModel.setHeaderData(7, QtCore.Qt.Horizontal, "Dest. Airport")

    def populateAirlineComboBoxes(self):
        query = QtSql.QSqlQuery()
        query.exec("SELECT name FROM Airlines")
        self.airlineComboBox.addItem("ANY")
        self.pbAirlineComboBox.addItem("ANY")
        self.cbAirlineComboBox.addItem("ANY")

        while query.next():
            self.airlineComboBox.addItem(query.value(0))
            self.pbAirlineComboBox.addItem(query.value(0))
            self.cbAirlineComboBox.addItem(query.value(0))

    def populatePAModel(self):
        query = QtSql.QSqlQuery()
        queryStr = "SELECT pid, uname, fname, lname, dob FROM Passengers WHERE 1=1"

        binding = {}

        if self.paFirstNameEdit.text():
            firstName = self.paFirstNameEdit.text().strip()
            queryStr += " AND fname ILIKE :firstName"
            binding[":firstName"] = '%' + firstName + '%'

        if self.paLastNameEdit.text():
            lastName = self.paLastNameEdit.text().strip()
            queryStr += " AND lname ILIKE :lastName"
            binding[":lastName"] = '%' + lastName + '%'

        if self.paDOBEdit.date().isValid() and self.paDOBCheckBox.isChecked():
            dob = self.paDOBEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND dob = :dob"
            binding[":dob"] = dob

        query.prepare(queryStr)
        for name, value in binding.items():
            query.bindValue(name, value)

        if not query.exec_():
            QtWidgets.QMessageBox.warning(self, "Retrieving Passengers Error", f"Error retrieving passengers: {query.lastError().text()}")
        else:
            self.paModel.setQuery(query)

        # Update the model column names
        self.paModel.setHeaderData(0, QtCore.Qt.Horizontal, "Passenger ID")
        self.paModel.setHeaderData(1, QtCore.Qt.Horizontal, "Username")
        self.paModel.setHeaderData(2, QtCore.Qt.Horizontal, "First Name")
        self.paModel.setHeaderData(3, QtCore.Qt.Horizontal, "Last Name")
        self.paModel.setHeaderData(4, QtCore.Qt.Horizontal, "DOB")

    def populateCAModel(self):
        query = QtSql.QSqlQuery()
        queryStr = "SELECT cid, uname, fname, lname, dob, position FROM Crew WHERE 1=1"

        binding = {}

        if self.caFirstNameEdit.text():
            firstName = self.caFirstNameEdit.text().strip()
            queryStr += " AND fname ILIKE :firstName"
            binding[":firstName"] = '%' + firstName + '%'

        if self.caLastNameEdit.text():
            lastName = self.caLastNameEdit.text().strip()
            queryStr += " AND lname ILIKE :lastName"
            binding[":lastName"] = '%' + lastName + '%'

        if self.caDOBEdit.date().isValid() and self.caDOBCheckBox.isChecked():
            dob = self.caDOBEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND dob = :dob"
            binding[":dob"] = dob

        if self.caPositionEdit.text():
            position = self.caPositionEdit.text().strip()
            queryStr += " AND position ILIKE :position"
            binding[":position"] = '%' + position + '%'

        query.prepare(queryStr)
        for name, value in binding.items():
            query.bindValue(name, value)

        if not query.exec_():
            QtWidgets.QMessageBox.warning(self, "Retrieving Crew Error", f"Error retrieving crew: {query.lastError().text()}")
        else:
            self.caModel.setQuery(query)

        # Update the model column names
        self.caModel.setHeaderData(0, QtCore.Qt.Horizontal, "Passenger ID")
        self.caModel.setHeaderData(1, QtCore.Qt.Horizontal, "Username")
        self.caModel.setHeaderData(2, QtCore.Qt.Horizontal, "First Name")
        self.caModel.setHeaderData(3, QtCore.Qt.Horizontal, "Last Name")
        self.caModel.setHeaderData(4, QtCore.Qt.Horizontal, "DOB")
        self.caModel.setHeaderData(5, QtCore.Qt.Horizontal, "Position")


    @QtCore.Slot()
    def openAddFlightDialog(self) -> None:
        dialog = AddFlightDialog(False)
        dialog.exec()
        self.populateFlightsModel()

    @QtCore.Slot()
    def openModifyFlightDialog(self) -> None:
        selectedFlightIndex = self.flightsView.currentIndex()
        if not selectedFlightIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a flight to modify.")
            return

        flightRecord = self.flightsModel.record(selectedFlightIndex.row())
        flight_id = flightRecord.value("fid")
        
        dialog = AddFlightDialog(True, flight_id)
        dialog.exec()
        self.populateFlightsModel()

    @QtCore.Slot()
    def removeFlight(self) -> None:
        selectedFlightIndex = self.flightsView.currentIndex()
        if not selectedFlightIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a flight to remove.")
            return

        flightRecord = self.flightsModel.record(selectedFlightIndex.row())
        flight_id = flightRecord.value("fid")
        removeFlight(flight_id)
        self.populateFlightsModel()

    
    @QtCore.Slot()
    def deletePassenger(self) -> None:
        selectedPassengerIndex = self.paView.currentIndex()
        if not selectedPassengerIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select an account to remove.")
            return
        passenger = self.paModel.record(selectedPassengerIndex.row())
        passenger_id = passenger.value("pid")
        deletePassengerAccount(passenger_id)
        print(f"deleted account {passenger_id}")
        self.populatePAModel()

    @QtCore.Slot()
    def openPassengerBookingDialog(self) -> None:
        selectedFlightIndex = self.flightsView.currentIndex()
        if not selectedFlightIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a flight first.")
            return

        flightRecord = self.flightsModel.record(selectedFlightIndex.row())
        flight_id = flightRecord.value("fid")
        dialog = AddPassengerBookingDialog(flight_id)
        if dialog.exec():
            pid = dialog.getSelectedPassengerId()
            seat_num = dialog.getSelectedSeatNumber()

            num_bags = dialog.getSelectedNumberOfBags()
            addBooking(pid, flight_id, seat_num, num_bags)
        self.populatePBModel()


    @QtCore.Slot()
    def openCrewBookingDialog(self) -> None:
        selectedFlightIndex = self.flightsView.currentIndex()
        if not selectedFlightIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a flight first.")
            return
        flightRecord = self.flightsModel.record(selectedFlightIndex.row())
        flight_id = flightRecord.value("fid")
        dialog = AddCrewBookingDialog()
        if dialog.exec():
            crew_id = dialog.getSelectedCrewId()
            addCrewToFlight(crew_id, flight_id)
        
        self.populateCBModel()



    @QtCore.Slot()
    def modifyPassengerBooking(self) -> None:
        selectedBookingIndex = self.pbView.currentIndex()

        bookingRecord = self.pbModel.record(selectedBookingIndex.row())
        passenger_id = bookingRecord.value("pid")
        flight_id = bookingRecord.value("fid")
        old_seat_num = bookingRecord.value("seat_num")
        modifyBookingDialog = ModifyBookingDialog(passenger_id, flight_id, old_seat_num)
        if modifyBookingDialog.exec():
            new_seat_num = modifyBookingDialog.seatNumComboBox.currentText()
            if str(new_seat_num) != str(old_seat_num):
                changeSeat(passenger_id, flight_id, new_seat_num)
        self.populatePBModel()
    

    @QtCore.Slot()
    def removePassengerBooking(self) -> None:
        selectedBookingIndex = self.pbView.currentIndex()
        if not selectedBookingIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a booking to remove.")
            return

        bookingRecord = self.pbModel.record(selectedBookingIndex.row())
        passenger_id = bookingRecord.value("pid")
        flight_id = bookingRecord.value("fid")
        removeBooking(passenger_id, flight_id)
        self.populatePBModel()

    @QtCore.Slot()
    def createCrew(self) -> None:
        dialog = CreateCrewDialog()
        dialog.exec()
        self.populateCAModel()

    @QtCore.Slot()
    def deleteCrew(self) -> None:
        selectedCrewIndex = self.caView.currentIndex()
        if not selectedCrewIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a crew member to remove.")
            return
        crew = self.caModel.record(selectedCrewIndex.row())
        crew_id = crew.value("cid")
        deleteCrew(crew_id)
        self.populateCAModel()

    @QtCore.Slot()
    def removeCrewBooking(self) -> None:
        selectedBookingIndex = self.cbView.currentIndex()
        if not selectedBookingIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a booking to remove.")
            return

        bookingRecord = self.cbModel.record(selectedBookingIndex.row())
        crew_id = bookingRecord.value("cid")
        flight_id = bookingRecord.value("fid")
        removeCrewBooking(crew_id, flight_id)
        self.populateCBModel()
        
class AddFlightDialog(QtWidgets.QDialog):
    def __init__(self, modifyingFlight, flight_id=None) -> None:
        super().__init__()

        if not modifyingFlight:
            self.setWindowTitle("Airport Manager - Add Flight")
        else:
            self.setWindowTitle("Airport Manager - Modify Flight")

        self.layout = QtWidgets.QFormLayout(self)

        self.planeComboBox = QtWidgets.QComboBox()
        self.populatePlaneComboBox()
        self.layout.addRow("Plane:", self.planeComboBox)

        self.depTermLineEdit = QtWidgets.QLineEdit()
        self.depTermLineEdit.setMaxLength(3)
        self.layout.addRow("Departure Terminal:", self.depTermLineEdit)

        self.depDateTimeEdit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.layout.addRow("Departure Time:", self.depDateTimeEdit)

        self.arrTermLineEdit = QtWidgets.QLineEdit()
        self.arrTermLineEdit.setMaxLength(3)
        self.layout.addRow("Arrival Terminal:", self.arrTermLineEdit)

        self.arrDateTimeEdit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.layout.addRow("Arrival Time:", self.arrDateTimeEdit)

        self.destLineEdit = QtWidgets.QLineEdit()
        self.destLineEdit.setMaxLength(3)
        self.layout.addRow("Destination Airport:", self.destLineEdit)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addRow(buttonBox)
        
        
        self.modifyingFlight = modifyingFlight
        self.flight_id = flight_id

        if self.modifyingFlight:
            self.loadFlightData()

        # Update the buttonBox connection to a new method
        buttonBox.accepted.connect(self.submitFlight)

        self.resize(380, 180)

    def populatePlaneComboBox(self):
        query = QtSql.QSqlQuery()
        query.exec("SELECT plane_id FROM Planes")
        while query.next():
            self.planeComboBox.addItem(str(query.value(0)))

    def loadFlightData(self):
        if self.flight_id is not None:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM Schedule WHERE fid = ?")
            query.addBindValue(self.flight_id)
            if query.exec() and query.next():
                # Load data into the dialog's fields
                self.planeComboBox.setCurrentText(str(query.value(1)))
                self.depTermLineEdit.setText(query.value(2))
                self.depDateTimeEdit.setDateTime(query.value(3))
                self.arrTermLineEdit.setText(query.value(4))
                self.arrDateTimeEdit.setDateTime(query.value(5))
                self.destLineEdit.setText(query.value(6))
            else:
                QtWidgets.QMessageBox.warning(self, "Flight Data Error", f"Error loading flight data: {query.lastError().text()}")

    def submitFlight(self):
        if self.modifyingFlight:
            self.modifyFlight()
        else:
            self.addFlight()

    def addFlight(self):
        plane_id = self.planeComboBox.currentText()
        dep_time = self.depDateTimeEdit.dateTime()
        arr_time = self.arrDateTimeEdit.dateTime()

        conflict_query = QtSql.QSqlQuery()
        
        # Think this checks all potential overlaps but should double check
        conflict_query.prepare("""
            SELECT COUNT(*) FROM Schedule
            WHERE plane_id = ? AND (
                (dep_time BETWEEN ? AND ?) OR
                (arr_time BETWEEN ? AND ?) OR
                (? BETWEEN dep_time AND arr_time) OR
                (? BETWEEN dep_time AND arr_time)
            )
        """)
        conflict_query.addBindValue(plane_id)
        conflict_query.addBindValue(dep_time)
        conflict_query.addBindValue(arr_time)
        conflict_query.addBindValue(dep_time)
        conflict_query.addBindValue(arr_time)
        conflict_query.addBindValue(dep_time)
        conflict_query.addBindValue(arr_time)

        if not conflict_query.exec_():
            QtWidgets.QMessageBox.warning(self, "Scheduling Conflict Error", f"Error checking for scheduling conflicts: {conflict_query.lastError().text()}")
            return

        conflict_query.next()
        if conflict_query.value(0) > 0:
            QtWidgets.QMessageBox.warning(self, "Scheduling Conflict Error", "Scheduling conflict detected.")
            return

        insert_query = QtSql.QSqlQuery()
        insert_query.prepare("INSERT INTO Schedule (plane_id, dep_term, dep_time, arr_term, arr_time, dest_airport) VALUES (?, ?, ?, ?, ?, ?)")
        insert_query.addBindValue(plane_id)
        insert_query.addBindValue(self.depTermLineEdit.text())
        insert_query.addBindValue(dep_time)
        insert_query.addBindValue(self.arrTermLineEdit.text())
        insert_query.addBindValue(arr_time)
        insert_query.addBindValue(self.destLineEdit.text())
        
        if not insert_query.exec_():
            QtWidgets.QMessageBox.warning(self, "Adding Flight Error", f"Error adding flight: {insert_query.lastError().text()}")


    def modifyFlight(self):
        if self.flight_id is None:
            return
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE Schedule SET plane_id = ?, dep_term = ?, dep_time = ?, arr_term = ?, arr_time = ?, dest_airport = ? WHERE fid = ?")
        query.addBindValue(self.planeComboBox.currentText())
        query.addBindValue(self.depTermLineEdit.text())
        query.addBindValue(self.depDateTimeEdit.dateTime())
        query.addBindValue(self.arrTermLineEdit.text())
        query.addBindValue(self.arrDateTimeEdit.dateTime())
        query.addBindValue(self.destLineEdit.text())
        query.addBindValue(self.flight_id)
        if not query.exec():
            QtWidgets.QMessageBox.warning(self, "Modifying Flight Error", f"Error modifying flight: {query.lastError().text()}")


class AddPassengerBookingDialog(QtWidgets.QDialog):
    def __init__(self, flight_id) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Add Passenger Booking")

        self.layout = QtWidgets.QFormLayout(self)

        self.passengersComboBox = QtWidgets.QComboBox()
        self.layout.addRow("Passenger:", self.passengersComboBox)
        self.populatePassengersComboBox()

        self.seatNumComboBox = QtWidgets.QComboBox()
        availableSeats = getAvailableSeats(flight_id)

        # Populate the combo box with available seats
        for seat in availableSeats:
            self.seatNumComboBox.addItem(str(seat))

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

    def populatePassengersComboBox(self):
        query = QtSql.QSqlQuery()
        query.exec("SELECT * FROM Passengers")
        while query.next():
            name = f"{query.value(1)} {query.value(2)} (ID: {query.value(0)})"
            self.passengersComboBox.addItem(name)

    def getSelectedPassengerId(self):
        # Get the selected passenger text
        selectedText = self.passengersComboBox.currentText()
        # Extract the passenger ID from the text
        passengerId = selectedText.split(" (ID: ")[-1].rstrip(")")
        return int(passengerId)

    def getSelectedSeatNumber(self):
        return int(self.seatNumComboBox.currentText())

    def getSelectedNumberOfBags(self):
        return int(self.bagNumComboBox.currentText())

class CreateCrewDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Create Crew")

        self.layout = QtWidgets.QFormLayout(self)

        self.firstNameLineEdit = QtWidgets.QLineEdit()
        self.firstNameLineEdit.setMaxLength(31)
        self.layout.addRow("First Name:", self.firstNameLineEdit)

        self.lastNameLineEdit = QtWidgets.QLineEdit()
        self.lastNameLineEdit.setMaxLength(31)
        self.layout.addRow("Last Name:", self.lastNameLineEdit)

        self.dobDateEdit = QtWidgets.QDateEdit()
        self.layout.addRow("Date of Birth:", self.dobDateEdit)

        self.positionEdit = QtWidgets.QLineEdit()
        self.positionEdit.setMaxLength(31)
        self.layout.addRow("Position:", self.positionEdit)

        self.signUpUsernameLineEdit = QtWidgets.QLineEdit()
        self.signUpUsernameLineEdit.setMaxLength(31)
        self.layout.addRow("Username:", self.signUpUsernameLineEdit)

        self.signUpPasswordLineEdit = QtWidgets.QLineEdit()
        self.signUpPasswordLineEdit.setMaxLength(31)
        self.signUpPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.layout.addRow("Password:", self.signUpPasswordLineEdit)

        createAccountButton = QtWidgets.QPushButton("Create Account")
        createAccountButton.clicked.connect(self.createAccountButtonClicked)
        self.layout.addRow(createAccountButton)

    @QtCore.Slot()
    def createAccountButtonClicked(self) -> None:
        firstName = self.firstNameLineEdit.text().strip()
        lastName = self.lastNameLineEdit.text().strip()
        dob = self.dobDateEdit.date().toString("yyyy-MM-dd")
        position = self.positionEdit.text().strip()
        username = self.signUpUsernameLineEdit.text().strip()
        password = self.signUpPasswordLineEdit.text().strip()

        createAccount(firstName, lastName, dob, position, username, password)
        self.accept()

def createAccount(firstName, lastName, dob, position, username, password):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO Crew (fname, lname, dob, position, uname, pswd) VALUES (?, ?, ?, ?, ?, ?)")
    query.addBindValue(firstName)
    query.addBindValue(lastName)
    query.addBindValue(dob)
    query.addBindValue(position)
    query.addBindValue(username)
    query.addBindValue(password)
    
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Create Account Error", f"Failed to create account: {query.lastError().text()}")
    else:
        print(f"Created account successfully")
        
class AddCrewBookingDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Add Crew Booking")

        self.layout = QtWidgets.QFormLayout(self)

        self.crewComboBox = QtWidgets.QComboBox()
        self.layout.addRow("Crew Member:", self.crewComboBox)
        self.populateCrewComboBox()

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addRow(buttonBox)
        
    def populateCrewComboBox(self):
        query = QtSql.QSqlQuery()
        query.exec("SELECT cid, fname, lname FROM Crew")
        while query.next():
            name = f"{query.value(1)} {query.value(2)} (ID: {query.value(0)})"
            self.crewComboBox.addItem(name)

    def getSelectedCrewId(self):
        # Get the selected crew text
        selectedText = self.crewComboBox.currentText()
        # Extract the crew ID from the text
        crewId = selectedText.split(" (ID: ")[-1].rstrip(")")
        return int(crewId)


def deletePassengerAccount(pid):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Passengers WHERE pid = ?")
    query.addBindValue(pid)
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Deleting Account Error", f"Error deleting passenger account: {query.lastError().text()}")

def deleteCrew(cid):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Crew WHERE cid = ?")
    query.addBindValue(cid)
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Deleting Account Error", f"Error deleting crew account: {query.lastError().text()}")
    else:
        print(f"deleted crew member {cid}")

def removeCrewBooking(cid, fid):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM CrewBookings WHERE cid = ? and fid = ?")
    query.addBindValue(cid)
    query.addBindValue(fid)
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Removing Booking Error", f"Error removing crew booking: {query.lastError().text()}")

def addCrewToFlight(crew_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO CrewBookings (cid, fid) VALUES (?, ?)")
    query.addBindValue(crew_id)
    query.addBindValue(flight_id)
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Adding Crew Error", f"Error adding crew to flight: {query.lastError().text()}")

def removePassengerFromFlight(passenger_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Bookings WHERE pid = ? AND fid = ?")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Removing Passenger Error", f"Error removing passenger from flight: {query.lastError().text()}")

def changeSeatOnFlight(passenger_id, flight_id, new_seat_id):
    query = QtSql.QSqlQuery()
    query.prepare("UPDATE Bookings SET seat_num = ? WHERE pid = ? AND fid = ?")
    query.addBindValue(new_seat_id)
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Changing Seat Error", f"Error changing seat: {query.lastError().text()}")

def addBag(passenger_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO Bags (pid, fid) VALUES (?, ?)")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Adding Bag Error", f"Error adding bag: {query.lastError().text()}")

def removeBag(bag_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Bags WHERE bid = ?")
    query.addBindValue(bag_id)
    if not query.exec():
        QtWidgets.QMessageBox.warning(None, "Removing Bag Error", f"Error removing bag: {query.lastError().text()}")

def viewCrewSchedules(self):
    query = QtSql.QSqlQuery()
    query.prepare("""SELECT c.fname, c.lname, c.cid, p.model_name, s.dep_term, s.dep_time, s.arr_term, s.arr_time, s.dest_airport
                     FROM Crew c, CrewBookings cb, Schedule s, Plane p
                     WHERE c.cid = cb.cid AND cb.fid = s.fid AND s.plane_id = p.plane_id""")
    if not query.exec():
        QtWidgets.QMessageBox.warning(self, "Viewing Schedule Error", f"Error viewing crew schedules: {query.lastError().text()}")
    else:
        # NEED TO FIGURE OUT HOW TO DISPLAY
        self.crewSchedulesModel.setQuery(query)

def getPassengersByAirlineAndDate(self, airline_name, date):
    query = QtSql.QSqlQuery()
    query.prepare("""SELECT fname, lname, pid
                     FROM Passengers NATURAL JOIN Bookings NATURAL JOIN Schedule NATURAL JOIN Planes NATURAL JOIN Airlines a
                     WHERE a.name = ? AND CAST(dep_time AS DATE) = ?""")
    query.addBindValue(airline_name)
    query.addBindValue(date)
    if not query.exec():
        QtWidgets.QMessageBox.warning(self, "Retrieving Passengers Error", f"Error retrieving passengers: {query.lastError().text()}")
    else:
        self.passengersModel.setQuery(query)
        
def removeFlight(flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Schedule WHERE fid = ?")
    query.addBindValue(flight_id)
    if not query.exec():
        QtWidgets.QMessageBox.critical(None, "Error", "Failed to remove flight: " + query.lastError().text())
