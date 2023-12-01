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
        self.bookFlightsButton = QtWidgets.QPushButton("Book Flight")
        self.bookFlightsButton.clicked.connect(self.openBookFlightDialog)
        flightsButtonLayout.addWidget(self.bookFlightsButton)

        # Bookings tab
        bookingsVLayout = QtWidgets.QVBoxLayout(bookingsTab)
        
        self.bookingsModel = QtSql.QSqlQueryModel()
        self.bookingsView = QtWidgets.QTableView()
        self.bookingsView.setModel(self.bookingsModel)
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

    @QtCore.Slot()
    def openBookFlightDialog(self) -> None:
        bookFlightDialog = BookFlightDialog()
        if bookFlightDialog.exec():
            print("Add booking to database")
    
    @QtCore.Slot()
    def openModifyBookingDialog(self) -> None:
        modifyBookingDialog = ModifyBookingDialog()
        if modifyBookingDialog.exec():
            print("Modify booking in database")
    
    @QtCore.Slot()
    def removeBooking(self) -> None:
        print("Remove booking here")

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

class ModifyBookingDialog(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Airport Manager - Modify Booking")

        self.layout = QtWidgets.QFormLayout(self)

        self.seatNumComboBox = QtWidgets.QComboBox()
        for i in range(1, 51):
            self.seatNumComboBox.addItem(str(i))
        self.layout.addRow("Seat:", self.seatNumComboBox)

        self.layout.addRow(QtWidgets.QLabel("Bags:"))
        self.bagsModel = QtSql.QSqlQueryModel()
        self.bagsView = QtWidgets.QTableView()
        self.bagsView.setModel(self.bagsModel)
        self.layout.addRow(self.bagsView)

        bagsButtonLayout = QtWidgets.QHBoxLayout()
        self.layout.addRow(bagsButtonLayout)
        bagsButtonLayout.addStretch()

        self.addBagButton = QtWidgets.QPushButton("Add Bag")
        bagsButtonLayout.addWidget(self.addBagButton)

        self.removeBagButton = QtWidgets.QPushButton("Remove Bag")
        bagsButtonLayout.addWidget(self.removeBagButton)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok, QtCore.Qt.Horizontal)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addRow(buttonBox)

        self.resize(460, 320)


def addBooking(self, passenger_id, flight_id, seat_num):
    query = QtSql.QSqlQuery()
    query.prepare("INSERT INTO Bookings (pid, fid, seat_num) VALUES (?, ?, ?)")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    query.addBindValue(seat_num)
    if not query.exec():
        print("Error adding booking:", query.lastError().text())

def removeBooking(self, passenger_id, flight_id):
    query = QtSql.QSqlQuery()
    query.prepare("DELETE FROM Bookings WHERE pid = ? AND fid = ?")
    query.addBindValue(passenger_id)
    query.addBindValue(flight_id)
    if not query.exec():
        print("Error removing booking:", query.lastError().text())

def changeFlight(self, passenger_id, old_flight_id, new_flight_id, new_seat_num):
    query = QtSql.QSqlQuery()
    query.exec("BEGIN;")

    # Check flight capacity
    query.prepare("""SELECT m.capacity 
                     FROM Models m 
                     JOIN Planes p ON m.model_name = p.model_name 
                     JOIN Schedule s ON p.plane_id = s.plane_id 
                     WHERE s.fid = ?""")
    query.addBindValue(new_flight_id)
    if not query.exec():
        print("Error checking flight capacity:", query.lastError().text())
        query.exec("ROLLBACK;")
        return

    if query.next():
        flight_capacity = query.value(0)
    else:
        print("Flight not found.")
        query.exec("ROLLBACK;")
        return

    # Check current bookings
    query.prepare("SELECT COUNT(*) FROM Bookings WHERE fid = ?")
    query.addBindValue(new_flight_id)
    if not query.exec():
        print("Error checking current bookings:", query.lastError().text())
        query.exec("ROLLBACK;")
        return

    if query.next():
        current_bookings = query.value(0)
    else:
        print("No bookings found.")
        query.exec("ROLLBACK;")
        return

    if current_bookings >= flight_capacity:
        print("Error: Adding to new flight exceeds capacity.")
        query.exec("ROLLBACK;")
        return

    # Delete from old flight
    query.prepare("DELETE FROM Bookings WHERE pid = ? AND fid = ?")
    query.addBindValue(passenger_id)
    query.addBindValue(old_flight_id)
    if not query.exec():
        print("Error deleting from old flight:", query.lastError().text())
        query.exec("ROLLBACK;")
        return

    # Insert into new flight
    query.prepare("INSERT INTO Bookings (pid, fid, seat_num) VALUES (?, ?, ?)")
    query.addBindValue(passenger_id)
    query.addBindValue(new_flight_id)
    query.addBindValue(new_seat_num)
    if not query.exec():
        print("Error inserting into new flight:", query.lastError().text())
        query.exec("ROLLBACK;")
        return

    # Update bags
    query.prepare("UPDATE Bags SET fid = ? WHERE pid = ? AND fid = ?")
    query.addBindValue(new_flight_id)
    query.addBindValue(passenger_id)
    query.addBindValue(old_flight_id)
    if not query.exec():
        print("Error updating baggage details:", query.lastError().text())
        query.exec("ROLLBACK;")
        return

    query.exec("COMMIT;")
    print("Flight changed successfully")
    

def changeSeat(self, passenger_id, flight_id, new_seat_num):
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