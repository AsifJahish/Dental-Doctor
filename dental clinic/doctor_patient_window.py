from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QGridLayout, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from db_connection import get_connection


class DoctorPatientWindow(QWidget):
    def __init__(self, doctor_username):
        super().__init__()
        self.doctor_username = doctor_username

        self.setWindowTitle(f"Patients - Dr. {doctor_username}")
        self.setGeometry(300, 80, 900, 650)

        main_layout = QVBoxLayout()

        # -------------------- SEARCH & FILTERS --------------------
        filter_layout = QGridLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Search by Name")

        self.search_phone = QLineEdit()
        self.search_phone.setPlaceholderText("Search by Phone")

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())

        btn_filter = QPushButton("Apply Filters")
        btn_filter.clicked.connect(self.apply_filters)

        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.load_patients)

        filter_layout.addWidget(QLabel("Name:"), 0, 0)
        filter_layout.addWidget(self.search_name, 0, 1)
        filter_layout.addWidget(QLabel("Phone:"), 0, 2)
        filter_layout.addWidget(self.search_phone, 0, 3)

        filter_layout.addWidget(QLabel("From Date:"), 1, 0)
        filter_layout.addWidget(self.date_from, 1, 1)
        filter_layout.addWidget(QLabel("To Date:"), 1, 2)
        filter_layout.addWidget(self.date_to, 1, 3)

        filter_layout.addWidget(btn_filter, 2, 1)
        filter_layout.addWidget(btn_refresh, 2, 2)

        main_layout.addLayout(filter_layout)

        # -------------------- PATIENT TABLE --------------------
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Phone", "Address"])
        self.table.setColumnWidth(1, 180)
        main_layout.addWidget(self.table)

        # -------------------- ADD NEW PATIENT --------------------
        add_layout = QGridLayout()

        self.new_name = QLineEdit()
        self.new_age = QLineEdit()
        self.new_phone = QLineEdit()
        self.new_address = QLineEdit()

        add_layout.addWidget(QLabel("Name:"), 0, 0)
        add_layout.addWidget(self.new_name, 0, 1)

        add_layout.addWidget(QLabel("Age:"), 1, 0)
        add_layout.addWidget(self.new_age, 1, 1)

        add_layout.addWidget(QLabel("Phone:"), 2, 0)
        add_layout.addWidget(self.new_phone, 2, 1)

        add_layout.addWidget(QLabel("Address:"), 3, 0)
        add_layout.addWidget(self.new_address, 3, 1)

        btn_add = QPushButton("Add Patient")
        btn_add.clicked.connect(self.add_patient)
        add_layout.addWidget(btn_add, 4, 1)

        main_layout.addLayout(add_layout)

        self.setLayout(main_layout)

        # Load initial data
        self.load_patients()

    # -------------------- LOAD PATIENTS --------------------
    def load_patients(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, contact, address FROM patients ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.populate_table(rows)

    # -------------------- FILTER --------------------
    def apply_filters(self):
        name = self.search_name.text().strip()
        phone = self.search_phone.text().strip()

        from_date = self.date_from.date().toString("yyyy-MM-dd")
        to_date = self.date_to.date().toString("yyyy-MM-dd")

        query = """
            SELECT id, name, age, contact, address 
            FROM patients
            WHERE (name ILIKE %s OR %s = '')
            AND (contact ILIKE %s OR %s = '')
            AND (created_at::date BETWEEN %s AND %s)
            ORDER BY id DESC
        """

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            query,
            (f"%{name}%", name, f"%{phone}%", phone, from_date, to_date)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.populate_table(rows)

    # -------------------- POPULATE TABLE --------------------
    def populate_table(self, rows):
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    # -------------------- ADD NEW PATIENT --------------------
    def add_patient(self):
        name = self.new_name.text()
        age = self.new_age.text()
        phone = self.new_phone.text()
        address = self.new_address.text()

        if name == "":
            QMessageBox.warning(self, "Error", "Name is required")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO patients (name, age, contact, address, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (name, age, phone, address))
        conn.commit()
        cur.close()
        conn.close()

        QMessageBox.information(self, "Success", "Patient added!")
        self.clear_add_fields()
        self.load_patients()

    def clear_add_fields(self):
        self.new_name.clear()
        self.new_age.clear()
        self.new_phone.clear()
        self.new_address.clear()
