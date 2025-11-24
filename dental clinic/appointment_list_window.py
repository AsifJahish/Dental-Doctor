from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QDateEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QDate, QTimer
from db_connection import get_connection

from appointment_window import AppointmentWindow



class AppointmentListPage(QWidget):
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id


        layout = QVBoxLayout()

        # -----------------------------
        # SEARCH BAR + DATE FILTER
        # -----------------------------
        search_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by patient name...")
        self.search_box.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_box)

        # Date filter
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.dateChanged.connect(self.load_appointments)
        search_layout.addWidget(self.date_filter)

        layout.addLayout(search_layout)

        # -----------------------------
        # APPOINTMENT TABLE
        # -----------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Patient", "Date", "Time", "Treatment"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # -----------------------------
        # BUTTONS
        # -----------------------------
        btn_layout = QHBoxLayout()

        btn_add = QPushButton("Add Appointment")
        btn_add.clicked.connect(self.add_appointment)

        btn_edit = QPushButton("Edit Selected")
        btn_edit.clicked.connect(self.edit_appointment)

        btn_delete = QPushButton("Delete Selected")
        btn_delete.clicked.connect(self.delete_appointment)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # AUTO-REFRESH
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_appointments)
        self.timer.start(1000)

        self.load_appointments()

    # -----------------------------------------------------------
    # LOAD APPOINTMENTS
    # -----------------------------------------------------------
    def load_appointments(self):
        selected_date = self.date_filter.date().toString("yyyy-MM-dd")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, p.name, a.date, a.time, a.treatment
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            WHERE a.doctor_id = %s AND a.date = %s
            ORDER BY a.time ASC;
        """, (self.doctor_id, selected_date))

        rows = cur.fetchall()
        self.table.setRowCount(len(rows))

        for r, row_data in enumerate(rows):
            for c, value in enumerate(row_data):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_appointments)
        self.timer.start(10) 

        cur.close()
        conn.close()

    # -----------------------------------------------------------
    # FILTER BY PATIENT NAME
    # -----------------------------------------------------------
    def filter_table(self):
        filter_text = self.search_box.text().lower()

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item:
                name = item.text().lower()
                self.table.setRowHidden(row, filter_text not in name)

    # -----------------------------------------------------------
    # ADD APPOINTMENT
    # -----------------------------------------------------------
    def add_appointment(self):
        self.window = AppointmentWindow(self.doctor_id)
        self.window.show()

    # -----------------------------------------------------------
    # EDIT SELECTED APPOINTMENT
    # -----------------------------------------------------------
    def edit_appointment(self):
        row = self.table.currentRow()
        if row < 0:
            return

        appt_id = self.table.item(row, 0).text()

        self.window = AppointmentWindow(self.doctor_id, appt_id)  # pass ID for edit mode
        self.window.show()

    # -----------------------------------------------------------
    # DELETE SELECTED APPOINTMENT
    # -----------------------------------------------------------
    def delete_appointment(self):
        row = self.table.currentRow()
        if row < 0:
            return

        appt_id = self.table.item(row, 0).text()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM appointments WHERE id = %s", (appt_id,))
        conn.commit()
        cur.close()
        conn.close()

        QMessageBox.information(self, "Deleted", "Appointment deleted.")
        self.load_appointments()
