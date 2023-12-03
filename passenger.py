from PySide6 import QtCore, QtWidgets, QtSql

class PassengerWindow(QtWidgets.QMainWindow):
    def __init__(self, passenger_id) -> None:
        super().__init__()
        self.passenger_id = passenger_id

        self.setWindowTitle("Airport Manager")

        tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(tabWidget)

        flightsTab = QtWidgets.QWidget()
        tabWidget.addTab(flightsTab, "Flights")

        bookingsTab = QtWidgets.QWidget()
        tabWidget.addTab(bookingsTab, "Bookings")

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
        
        # Select rows instead of cells
        self.flightsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.flightsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
        flightsVLayout.addWidget(self.flightsView)

        flightsButtonLayout = QtWidgets.QHBoxLayout()
        flightsVLayout.addLayout(flightsButtonLayout)
        flightsButtonLayout.addStretch()
        self.bookFlightsButton = QtWidgets.QPushButton("Book Flight")
        self.bookFlightsButton.clicked.connect(self.openBookFlightDialog)
        flightsButtonLayout.addWidget(self.bookFlightsButton)

        # Bookings tab
        bookingsVLayout = QtWidgets.QVBoxLayout(bookingsTab)
        
        self.bookingsModel = QtSql.QSqlQueryModel()
        self.bookingsView = QtWidgets.QTableView()
        self.bookingsView.setModel(self.bookingsModel)
        
        # Select rows instead of cells
        self.bookingsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.bookingsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        bookingsVLayout.addWidget(self.bookingsView)        

        bookingsButtonLayout = QtWidgets.QHBoxLayout()
        bookingsVLayout.addLayout(bookingsButtonLayout)
        bookingsButtonLayout.addStretch()
        
        self.modifyBookingButton = QtWidgets.QPushButton("Modify Booking")
        self.modifyBookingButton.clicked.connect(self.openModifyBookingDialog)
        bookingsButtonLayout.addWidget(self.modifyBookingButton)
        
        self.removeBookingButton = QtWidgets.QPushButton("Remove Booking")
        self.removeBookingButton.clicked.connect(self.removeBooking)
        bookingsButtonLayout.addWidget(self.removeBookingButton)

        self.resize(1120, 590)

        self.airlineComboBox.currentIndexChanged.connect(self.updateFlightsView)
        self.fromDateEdit.dateChanged.connect(self.updateFlightsView)
        self.toDateEdit.dateChanged.connect(self.updateFlightsView)
        self.fromCheckBox.stateChanged.connect(self.updateFlightsView)
        self.toCheckBox.stateChanged.connect(self.updateFlightsView)
        self.destinationLineEdit.textChanged.connect(self.updateFlightsView)

        self.updateFlightsView()
        self.updateBookingsView()
        
        self.populateAirlinesIntoComboBox()

    def updateFlightsView(self):
        queryStr = "SELECT s.fid, s.dep_term, s.dep_time, s.arr_term, s.arr_time, s.dest_airport, p.model_name, a.name " \
                "FROM Schedule s " \
                "JOIN Planes p ON s.plane_id = p.plane_id " \
                "JOIN Airlines a ON p.aid = a.aid WHERE 1=1"
        binding = {}

        if self.fromCheckBox.isChecked():
            fromDate = self.fromDateEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND s.dep_time >= :fromDate"
            binding[':fromDate'] = fromDate

        if self.toCheckBox.isChecked():
            toDate = self.toDateEdit.date().toString("yyyy-MM-dd")
            queryStr += " AND s.dep_time <= :toDate"
            binding[":toDate"] = toDate

        if self.airlineComboBox.currentIndex() != 0:
            airline = self.airlineComboBox.currentText()
            queryStr += " AND a.name = :airline"
            binding[":airline"] = airline

        if self.destinationLineEdit.text():
            destination = "%" + self.destinationLineEdit.text().strip() + "%"
            queryStr += " AND s.dest_airport ILIKE :destination"
            binding[":destination"] = destination

        query = QtSql.QSqlQuery()
        query.prepare(queryStr)
        for name, value in binding.items():
            query.bindValue(name, value)

        if not query.exec_():
            print("Error updating flights view:", query.lastError().text())
        else:
            self.flightsModel.setQuery(query)
            self.flightsModel.layoutChanged.emit()  # Notify the view that the layout has changed

    def updateBookingsView(self):
        queryStr = """
        SELECT b.fid, s.dep_term, s.dep_time, s.arr_term, s.arr_time, s.dest_airport, p.model_name, a.name, b.seat_num, COUNT(bg.bid) AS bags
        FROM Bookings b
        LEFT JOIN Schedule s ON b.fid = s.fid
        LEFT JOIN Planes p ON s.plane_id = p.plane_id
        LEFT JOIN Airlines a ON p.aid = a.aid
        LEFT JOIN Bags bg ON b.pid = bg.pid AND b.fid = bg.fid
        WHERE b.pid = :passenger_id
        GROUP BY b.fid, s.dep_term, s.dep_time, s.arr_term, s.arr_time, s.dest_airport, p.model_name, a.name, b.seat_num
        ORDER BY s.dep_time
        """

        query = QtSql.QSqlQuery()
        query.prepare(queryStr)
        query.bindValue(":passenger_id", self.passenger_id)

        if not query.exec_():
            print("Error updating bookings view:", query.lastError().text())
        else:
            self.bookingsModel.setQuery(query)
            self.bookingsModel.layoutChanged.emit()  # Notify the view that the layout has changed


    def populateAirlinesIntoComboBox(self):
        query = QtSql.QSqlQuery("SELECT name FROM Airlines")
        self.airlineComboBox.addItem("ANY")
        while query.next():
            self.airlineComboBox.addItem(query.value(0))

    @QtCore.Slot()
    def openBookFlightDialog(self) -> None:
        selectedFlightIndex = self.flightsView.currentIndex()
        if not selectedFlightIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a flight to book.")
            return

        flight_id = self.flightsModel.record(selectedFlightIndex.row()).value("fid")
        passenger_id = self.passenger_id
        bookFlightDialog = BookFlightDialog(flight_id)
        if bookFlightDialog.exec():
            seat_num = bookFlightDialog.seatNumComboBox.currentText()
            num_bags = bookFlightDialog.bagNumComboBox.currentText()

            addBooking(passenger_id, flight_id, seat_num, num_bags)
        self.updateBookingsView()
    
    @QtCore.Slot()
    def openModifyBookingDialog(self) -> None:
        selectedBookingIndex = self.bookingsView.currentIndex()
        if not selectedBookingIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a booking to modify.")
            return

        bookingRecord = self.bookingsModel.record(selectedBookingIndex.row())
        flight_id = bookingRecord.value("fid")
        old_seat_num = bookingRecord.value("seat_num")
        
        modifyBookingDialog = ModifyBookingDialog(self.passenger_id, flight_id, old_seat_num)
        if modifyBookingDialog.exec():
            new_seat_num = modifyBookingDialog.seatNumComboBox.currentText()
            if str(new_seat_num) != str(old_seat_num):
                changeSeat(self.passenger_id, flight_id, new_seat_num)
        self.updateBookingsView()
    
    @QtCore.Slot()
    def removeBooking(self) -> None:
        selectedBookingIndex = self.bookingsView.currentIndex()
        if not selectedBookingIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a booking to remove.")
            return

        bookingRecord = self.bookingsModel.record(selectedBookingIndex.row())
        flight_id = bookingRecord.value("fid")
        removeBooking(self.passenger_id, flight_id)
        self.updateBookingsView()

class BookFlightDialog(QtWidgets.QDialog):
    def __init__(self, flight_id) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Book Flight")

        self.layout = QtWidgets.QFormLayout(self)

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

class ModifyBookingDialog(QtWidgets.QDialog):
    def __init__(self, passenger_id, flight_id, seat_num) -> None:
        super().__init__()
        self.passenger_id, self.flight_id = passenger_id, flight_id

        self.setWindowTitle("Airport Manager - Modify Booking")

        self.layout = QtWidgets.QFormLayout(self)

        self.seatNumComboBox = QtWidgets.QComboBox()
        availableSeats = getAvailableSeats(self.flight_id, seat_num)
        for seat in availableSeats:
            self.seatNumComboBox.addItem(str(seat))
        if int(seat_num) in availableSeats:
            self.seatNumComboBox.setCurrentIndex(availableSeats.index(int(seat_num)))
        else:
            self.seatNumComboBox.setCurrentIndex(0)

        self.layout.addRow("Seat:", self.seatNumComboBox)

        self.layout.addRow(QtWidgets.QLabel("Bags:"))
        self.bagsModel = QtSql.QSqlQueryModel()
        self.bagsView = QtWidgets.QTableView()
        self.bagsView.setModel(self.bagsModel)

        # Select rows instead of cells
        self.bagsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.bagsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
        self.layout.addRow(self.bagsView)

        bagsButtonLayout = QtWidgets.QHBoxLayout()
        self.layout.addRow(bagsButtonLayout)
        bagsButtonLayout.addStretch()

        self.addBagButton = QtWidgets.QPushButton("Add Bag")
        self.addBagButton.clicked.connect(self.onAddBag)
        bagsButtonLayout.addWidget(self.addBagButton)
        
        self.removeBagButton = QtWidgets.QPushButton("Remove Bag")
        self.removeBagButton.clicked.connect(self.onRemoveBag)
        bagsButtonLayout.addWidget(self.removeBagButton)

        self.updateBagsTable()


        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addRow(buttonBox)

        self.resize(460, 320)

    def updateBagsTable(self):
        query = QtSql.QSqlQuery()
        query.prepare("SELECT bid, pid, fid FROM Bags WHERE pid = :pid AND fid = :fid")
        query.bindValue(":pid", self.passenger_id)
        query.bindValue(":fid", self.flight_id)
        if not query.exec_():
            print("ERROR", query.lastError().text())
            return

        self.bagsModel.setQuery(query)
        self.bagsModel.layoutChanged.emit()  # Notify the view that the layout has changed
        if self.bagsModel.rowCount() >= 2:
            self.addBagButton.setDisabled(True)
        else:
            self.addBagButton.setEnabled(True)

    def onAddBag(self):
        addBag(self.passenger_id, self.flight_id)
        self.updateBagsTable()

    def onRemoveBag(self):
        selectedBagIndex = self.bagsView.currentIndex()
        if not selectedBagIndex.isValid():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select a bag to remove.")
            return

        bagRecord = self.bagsModel.record(selectedBagIndex.row())
        bag_id = bagRecord.value("bid")
        removeBag(bag_id)
        self.updateBagsTable()

# TABLE MODIFICATION QUERIES

def addBooking(passenger_id, flight_id, seat_num, num_bags):
    query = QtSql.QSqlQuery()
    query.exec("BEGIN;")  # Start transaction

    # Add the booking
    query.prepare("INSERT INTO Bookings (pid, fid, seat_num) VALUES (?, ?, ?)")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    query.addBindValue(seat_num)
    if not query.exec():
        print("Error adding booking:", query.lastError().text())
        query.exec("ROLLBACK;")  # Rollback if error occurs
        return

    # Add bags
    for _ in range(int(num_bags)):
        query.prepare("INSERT INTO Bags (pid, fid) VALUES (?, ?)")
        query.addBindValue(passenger_id)
        query.addBindValue(flight_id)
        if not query.exec():
            print("Error adding bag:", query.lastError().text())
            query.exec("ROLLBACK;")  # Rollback if error occurs
            return

    query.exec("COMMIT;")  # Commit the transaction
    print(f"Successfully added booking and bags, {passenger_id=} {flight_id=} {seat_num=} {num_bags=}")

def removeBooking(passenger_id, flight_id):
    query = QtSql.QSqlQuery()
    query.exec("BEGIN;")  # Start transaction

    # Delete bags associated with the booking
    query.prepare("DELETE FROM Bags WHERE pid = ? AND fid = ?")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error removing bags:", query.lastError().text())
        query.exec("ROLLBACK;")  # Rollback if error occurs
        return

    # Delete the booking
    query.prepare("DELETE FROM Bookings WHERE pid = ? AND fid = ?")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error removing booking:", query.lastError().text())
        query.exec("ROLLBACK;")  # Rollback if error occurs
        return

    query.exec("COMMIT;")  # Commit the transaction
    print(f"Successfully removed booking and associated bags, {passenger_id=} {flight_id=}")


def changeSeat(passenger_id, flight_id, new_seat_num):
    print(f"changing seat for {passenger_id} on {flight_id}")
    query = QtSql.QSqlQuery()
    query.exec("BEGIN;")

    # Check if new seat is available
    query.prepare("SELECT 1 FROM Bookings WHERE fid = ? AND seat_num = ?")
    query.addBindValue(flight_id)
    query.addBindValue(new_seat_num)
    if not query.exec():
        print("Error checking seat availability:", query.lastError().text())
        query.exec("ROLLBACK;")
        return

    if query.next():
        print("Seat not available")
        query.exec("ROLLBACK;")
        return

    # Update seat number
    query.prepare("UPDATE Bookings SET seat_num = ? WHERE pid = ? AND fid = ?")
    query.addBindValue(new_seat_num)
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error changing seat:", query.lastError().text())
        query.exec("ROLLBACK;")
        return

    query.exec("COMMIT;")
    print("Seat changed successfully")

def addBag(passenger_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO Bags (pid, fid) VALUES (?, ?)")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error adding bag:", query.lastError().text())
    else:
        print(f"Added bag, {passenger_id=} {flight_id=}")

def removeBag(bag_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Bags WHERE bid = ?")
    query.addBindValue(bag_id)
    if not query.exec():
        print("Error removing bag:", query.lastError().text())

def getAvailableSeats(flight_id, current_seat=None):
    # Query to get the model of the plane for the given flight
    query_plane_model = QtSql.QSqlQuery()
    query_plane_model.prepare("SELECT model_name FROM Planes INNER JOIN Schedule ON Planes.plane_id = Schedule.plane_id WHERE fid = ?")
    query_plane_model.addBindValue(flight_id)
    if not query_plane_model.exec_():
        print("Error fetching plane model:", query_plane_model.lastError().text())
        return []

    model_name = None
    if query_plane_model.next():
        model_name = query_plane_model.value(0)

    # Query to get the capacity of the plane model
    query_capacity = QtSql.QSqlQuery()
    query_capacity.prepare("SELECT capacity FROM Models WHERE model_name = ?")
    query_capacity.addBindValue(model_name)
    if not query_capacity.exec_():
        print("Error fetching plane capacity:", query_capacity.lastError().text())
        return []

    capacity = None
    if query_capacity.next():
        capacity = query_capacity.value(0)
    
    if capacity == None:
        print("Couldn't get plane capacity")
        return []

    # Query to get booked seats
    query_booked_seats = QtSql.QSqlQuery()
    query_booked_seats.prepare("SELECT seat_num FROM Bookings WHERE fid = ?")
    query_booked_seats.addBindValue(flight_id)
    if not query_booked_seats.exec_():
        print("Error fetching booked seats:", query_booked_seats.lastError().text())
        return []

    bookedSeats = set()
    while query_booked_seats.next():
        bookedSeats.add(query_booked_seats.value(0))

    totalSeats = set(range(1, capacity + 1))
    availableSeats = totalSeats - bookedSeats
    if current_seat:
        availableSeats.add(current_seat)
    return sorted(availableSeats)
