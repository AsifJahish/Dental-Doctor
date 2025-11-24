
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget
)
from PyQt5.QtCore import Qt
from db_connection import get_connection

from PyQt5.QtCore import Qt, QTimer

# from appointment_window import AppointmentListPage

from patient_window import PatientWindow


from appointment_list_window import AppointmentListPage


class DoctorDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Dental Clinic - Dr. {username}")
        self.setGeometry(200, 50, 1000, 600)

        self.doctor_id = self.get_doctor_id()

        main_layout = QHBoxLayout(self)

        # LEFT MENU
        left_menu = QVBoxLayout()

        lbl_title = QLabel(f"Dr. {username}")
        lbl_title.setStyleSheet("font-size:18px; font-weight:bold;")
        left_menu.addWidget(lbl_title)
        left_menu.addSpacing(30)

        # Patients Button
        btn_patients = QPushButton("Patients")
        btn_patients.clicked.connect(self.show_patients)
        left_menu.addWidget(btn_patients)

        # Appointments Button (SHOWS LIST ON RIGHT)
        btn_appointments = QPushButton("Appointments")
        btn_appointments.clicked.connect(self.show_appointments)
        left_menu.addWidget(btn_appointments)

        left_menu.addStretch()

        # STACKED PAGES
        self.stack = QStackedWidget()

        self.patient_page = self.create_patient_page()
        self.stack.addWidget(self.patient_page)

        self.appointment_page = AppointmentListPage(self.doctor_id)
        self.stack.addWidget(self.appointment_page)

        # ADD BOTH TO MAIN LAYOUT
        main_layout.addLayout(left_menu, 1)
        main_layout.addWidget(self.stack, 4)







    def show_appointments(self):
        self.stack.setCurrentWidget(self.appointment_page)

    # -------------------
    # Get doctor_id using logged-in username
    # -------------------
    def get_doctor_id(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM doctors WHERE username = %s", (self.username,))
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
        self.patient_table.setColumnCount(6)
        self.patient_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Phone", "Email", "Age", "Created"]
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


        btn_edit.clicked.connect(self.edit_selected_patient)
        btn_delete.clicked.connect(self.delete_selected_patient)



        page.setLayout(layout)
        self.load_patients()
        return page
    




    # =====================================================
    # PAGE SWITCHING
    # =====================================================

    

    def show_patients(self):
        self.stack.setCurrentWidget(self.patient_page)





    

    # =====================================================
    # LOAD DATA FROM DATABASE
    # =====================================================
    def load_patients(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, phone_number, email, age, created_at
            FROM patients
            ORDER BY id DESC;
        """)

        rows = cur.fetchall()
        self.patient_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_value in enumerate(row_data):
                self.patient_table.setItem(row_index, col_index, QTableWidgetItem(str(col_value)))
        
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_patients)
        self.timer.start(1000) 
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
        SELECT id, name, phone_number, email, age, created_at
        FROM patients
        WHERE name ILIKE %s OR phone_number ILIKE %s OR email ILIKE %s
        ORDER BY id DESC;
    """, (f"%{name_filter}%", f"%{name_filter}%", f"%{name_filter}%"))

        rows = cur.fetchall()
        self.patient_table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, col_value in enumerate(row_data):
                self.patient_table.setItem(row_index, col_index, QTableWidgetItem(str(col_value)))
        cur.close()
        conn.close()



    def open_add_patient_window(self):
        self.patient_window = PatientWindow()
        self.patient_window.show()
        # reload patient list after window closes
        self.patient_window.destroyed.connect(self.load_patients)




    def edit_selected_patient(self):
        row = self.patient_table.currentRow()
        if row < 0:
            return  # no selection

        patient_id = self.patient_table.item(row, 0).text()

        # Pass id to PatientWindow in edit mode
        self.patient_window = PatientWindow(patient_id=patient_id)
        self.patient_window.show()
        self.patient_window.destroyed.connect(self.load_patients)

    def delete_selected_patient(self):
        row = self.patient_table.currentRow()
        if row < 0:
            return  # no selection

        patient_id = self.patient_table.item(row, 0).text()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        conn.commit()
        cur.close()
        conn.close()

        self.load_patients()
