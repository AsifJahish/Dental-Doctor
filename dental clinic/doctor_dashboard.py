from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget
)
from PyQt5.QtCore import Qt
from db_connection import get_connection

from patient_window import PatientWindow 



class DoctorDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Dental Clinic - Dr. {username}")
        self.setGeometry(200, 50, 1000, 600)

        # Fetch doctor_id from database
        self.doctor_id = self.get_doctor_id(username)

        # ========== MAIN LAYOUT ==========
        main_layout = QHBoxLayout(self)

        # ---------- LEFT MENU ----------
        left_menu = QVBoxLayout()

        lbl_title = QLabel(f"Dr. {username}")
        lbl_title.setStyleSheet("font-size:18px; font-weight:bold;")
        left_menu.addWidget(lbl_title)
        left_menu.addSpacing(30)

        btn_patients = QPushButton("Patients")
        btn_patients.clicked.connect(self.show_patients)
        left_menu.addWidget(btn_patients)

        btn_appointments = QPushButton("Appointments")
        btn_appointments.clicked.connect(self.show_appointments)
        left_menu.addWidget(btn_appointments)

        left_menu.addStretch()

        # ---------- MAIN CONTENT ----------
        self.stack = QStackedWidget()

        self.patient_page = self.create_patient_page()
        self.appointment_page = self.create_appointment_page()

        self.stack.addWidget(self.patient_page)
        self.stack.addWidget(self.appointment_page)

        main_layout.addLayout(left_menu, 1)
        main_layout.addWidget(self.stack, 4)

    # -------------------
    # Get doctor_id from username
    # -------------------
    def get_doctor_id(self, username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM doctors WHERE username = %s", (username,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else None

    # =====================================================
    #   PATIENT PAGE
    # =====================================================
    def create_patient_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.patient_search = QLineEdit()
        self.patient_search.setPlaceholderText("Search patient by name...")
        self.patient_search.textChanged.connect(self.filter_patients)
        layout.addWidget(self.patient_search)

        self.patient_table = QTableWidget()
        self.patient_table.setColumnCount(5)
        self.patient_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Contact", "Age", "Created"]
        )
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.patient_table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Add Patient")
        btn_edit = QPushButton("Edit Selected")
        btn_delete = QPushButton("Delete Selected")

        btn_layout.addWidget(btn_add)
        btn_add.clicked.connect(self.open_add_patient_window) 
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        layout.addLayout(btn_layout)

        page.setLayout(layout)
        self.load_patients()
        return page

    # =====================================================
    #   APPOINTMENT PAGE
    # =====================================================
    def create_appointment_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.appointment_search = QLineEdit()
        self.appointment_search.setPlaceholderText("Search appointment by patient name...")
        self.appointment_search.textChanged.connect(self.filter_appointments)
        layout.addWidget(self.appointment_search)

        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(5)
        self.appointment_table.setHorizontalHeaderLabels(
            ["ID", "Patient", "Date", "Time", "Treatment"]
        )
        self.appointment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.appointment_table)

        page.setLayout(layout)
        self.load_appointments()
        return page

    # =====================================================
    # PAGE SWITCHING
    # =====================================================


    def show_patients(self):
        self.stack.setCurrentWidget(self.patient_page)

    def show_appointments(self):
        self.stack.setCurrentWidget(self.appointment_page)

    # =====================================================
    # LOAD DATA FROM DATABASE
    # =====================================================
    def load_patients(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, contact, age, created_at
            FROM patients
            ORDER BY id DESC;
        """)
        rows = cur.fetchall()
        self.patient_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_value in enumerate(row_data):
                self.patient_table.setItem(row_index, col_index, QTableWidgetItem(str(col_value)))
        cur.close()
        conn.close()

    def load_appointments(self):
        if not self.doctor_id:
            return  # doctor not found
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, p.name, a.date, a.time, a.treatment
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            WHERE a.doctor_id = %s
            ORDER BY a.date DESC;
        """, (self.doctor_id,))
        rows = cur.fetchall()
        self.appointment_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_value in enumerate(row_data):
                self.appointment_table.setItem(row_index, col_index, QTableWidgetItem(str(col_value)))
        cur.close()
        conn.close()

    # =====================================================
    # FILTER FUNCTIONS
    # =====================================================

    
    def filter_patients(self):
        name_filter = self.patient_search.text()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, contact, age, created_at
            FROM patients
            WHERE name ILIKE %s OR contact ILIKE %s
            ORDER BY id DESC;
        """, (f"%{name_filter}%", f"%{name_filter}%"))
        rows = cur.fetchall()
        self.patient_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_value in enumerate(row_data):
                self.patient_table.setItem(row_index, col_index, QTableWidgetItem(str(col_value)))
        cur.close()
        conn.close()

    def filter_appointments(self):
        filter_text = self.appointment_search.text().lower()
        for row in range(self.appointment_table.rowCount()):
            patient_item = self.appointment_table.item(row, 1)
            if patient_item:
                patient_name = patient_item.text().lower()
                self.appointment_table.setRowHidden(row, filter_text not in patient_name)


    def open_add_patient_window(self):
        self.patient_window = PatientWindow()
        self.patient_window.show()
        # reload patient list after window closes
        self.patient_window.destroyed.connect(self.load_patients)
