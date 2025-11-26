# from PyQt5.QtWidgets import (
#     QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
#     QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
#     QStackedWidget, QFrame, QMessageBox
# )
# from PyQt5.QtCore import Qt, QTimer
# from db_connection import get_connection
# from patient_window import PatientWindow
# from appointment_list_window import AppointmentListPage


# class DoctorDashboard(QWidget):
#     def __init__(self, username):
#         super().__init__()
#         self.username = username
#         self.setWindowTitle(f"Dental Clinic - Dr. {username}")
#         self.setGeometry(200, 50, 1200, 700)
#         self.setMinimumSize(2000, 1000)
#         self.setStyleSheet("background-color: #f4f6fa;")

#         self.doctor_id = self.get_doctor_id()

#         main_layout = QHBoxLayout(self)
#         main_layout.setContentsMargins(0, 0, 0, 0)

#         # --------------------------------------------------------
#         # LEFT SIDE MENU PANEL
#         # --------------------------------------------------------
#         left_panel = QFrame()
#         left_panel.setFixedWidth(300)
#         left_panel.setStyleSheet("""
#             QFrame {
#                 background-color: #2f4050;
#             }
#             QLabel {
#                 color: white;
#                 font-size: 25px;
#                 padding-left: 15px;
#             }
#             QPushButton {
#                 background-color: transparent;
#                 color: white;
#                 font-size: 25px;
#                 padding: 12px;
#                 text-align: left;
#                 border: none;
#             }
#             QPushButton:hover {
#                 background-color: #3c5065;
#             }
#         """)

#         left_layout = QVBoxLayout(left_panel)
#         left_layout.setSpacing(15)

#         # Doctor Name Header
#         title = QLabel(f"Dr. {username}")
#         title.setStyleSheet("font-size: 35px; font-weight: bold;")
#         left_layout.addWidget(title)
#         left_layout.addSpacing(20)

#         # Menu Buttons
#         btn_patients = QPushButton("🧑‍⚕️  Patients")
#         btn_appointments = QPushButton("📅  Appointments")

#         left_layout.addWidget(btn_patients)
#         left_layout.addWidget(btn_appointments)

#         left_layout.addStretch()

#         # --------------------------------------------------------
#         # RIGHT CONTENT STACK
#         # --------------------------------------------------------
#         self.stack = QStackedWidget()
#         self.patient_page = self.create_patient_page()
#         self.appointment_page = AppointmentListPage(self.doctor_id)

#         self.stack.addWidget(self.patient_page)
#         self.stack.addWidget(self.appointment_page)

#         # Add to main layout
#         main_layout.addWidget(left_panel)
#         main_layout.addWidget(self.stack)

#         # Button connections
#         btn_patients.clicked.connect(self.show_patients)
#         btn_appointments.clicked.connect(self.show_appointments)

#     # --------------------------------------------------------
#     # SWITCH PAGES
#     # --------------------------------------------------------
#     def show_patients(self):
#         self.stack.setCurrentWidget(self.patient_page)

#     def show_appointments(self):
#         self.stack.setCurrentWidget(self.appointment_page)

#     # --------------------------------------------------------
#     # GET DOCTOR ID
#     # --------------------------------------------------------
#     def get_doctor_id(self):
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT id FROM doctors WHERE username=%s", (self.username,))
#         result = cur.fetchone()
#         cur.close()
#         conn.close()
#         return result[0] if result else None

#     # --------------------------------------------------------
#     # PATIENT PAGE
#     # --------------------------------------------------------
#     def create_patient_page(self):
#         page = QWidget()
#         layout = QVBoxLayout()
#         layout.setContentsMargins(20, 20, 20, 20)

#         # Search Box
#         self.patient_search = QLineEdit()
#         self.patient_search.setPlaceholderText("Search patient by name, phone, or email...")
#         self.patient_search.setStyleSheet("""
#             QLineEdit {
#                 padding: 10px;
#                 border: 1px solid #d0d0d0;
#                 border-radius: 10px;
#                 font-size: 30px;
#             }
#         """)
#         self.patient_search.textChanged.connect(self.filter_patients)
#         layout.addWidget(self.patient_search)

#         # Table Container (Card style)
#         table_container = QFrame()
#         table_container.setStyleSheet("""
#             QFrame {
#                 background-color: white;
#                 border-radius: 35px;
#                 padding: 15px;
#             }
#         """)

#         table_layout = QVBoxLayout(table_container)

#         # Patient Table
#         self.patient_table = QTableWidget()
#         self.patient_table.setColumnCount(6)
#         self.patient_table.setHorizontalHeaderLabels(
#             ["ID", "Name", "Phone", "Email", "Age", "Created"]
#         )

#         self.patient_table.setMinimumWidth(1000)
#         self.patient_table.setMinimumHeight(1000)

#         self.patient_table.horizontalHeader().setFixedHeight(80)   # Bigger header
#         self.patient_table.verticalHeader().setDefaultSectionSize(40)  # Bigger rows



#         self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.patient_table.setStyleSheet("""
#             QTableWidget {
#                 background-color: white;
#                 border-radius: 30px;
#             }
#             QHeaderView::section {
#                 background-color: #e8edf2;
#                 padding: 6px;
#                 font-size: 30px;
#             }
#         """)
#         table_layout.addWidget(self.patient_table)
#         layout.addWidget(table_container)

#         # Buttons Row
#         btn_row = QHBoxLayout()
#         btn_row.setSpacing(15)

#         btn_add = QPushButton("➕  Add Patient")
#         btn_edit = QPushButton("✏️  Edit")
#         btn_delete = QPushButton("🗑️  Delete")

#         for btn in [btn_add, btn_edit, btn_delete]:
#             btn.setStyleSheet("""
#                 QPushButton {
#                     background-color: #2b7cff;
#                     color: white;
#                     padding: 10px;
#                     font-size: 30px;
#                     border-radius: 10px;
#                 }
#                 QPushButton:hover {
#                     background-color: #4f94ff;
#                 }
#             """)

#         btn_row.addWidget(btn_add)
#         btn_row.addWidget(btn_edit)
#         btn_row.addWidget(btn_delete)

#         layout.addLayout(btn_row)

#         # Connections
#         btn_add.clicked.connect(self.open_add_patient_window)
#         btn_edit.clicked.connect(self.edit_selected_patient)
#         btn_delete.clicked.connect(self.delete_selected_patient)

#         page.setLayout(layout)

#         self.load_patients()
#         return page

#     # --------------------------------------------------------
#     # LOAD PATIENTS
#     # --------------------------------------------------------
#     def load_patients(self):
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             SELECT id, name, phone_number, email, age, created_at
#             FROM patients
#             ORDER BY id DESC;
#         """)
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.load_patients)
#         self.timer.start(1000) 
#         rows = cur.fetchall()
#         cur.close()
#         conn.close()

#         self.patient_table.setRowCount(len(rows))
#         for row_i, row in enumerate(rows):
#             for col_i, col in enumerate(row):
#                 self.patient_table.setItem(row_i, col_i, QTableWidgetItem(str(col)))

#     # --------------------------------------------------------
#     # FILTER PATIENTS
#     # --------------------------------------------------------
#     def filter_patients(self):
#         val = self.patient_search.text()
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             SELECT id, name, phone_number, email, age, created_at
#             FROM patients
#             WHERE name ILIKE %s OR phone_number ILIKE %s OR email ILIKE %s
#             ORDER BY id DESC;
#         """, (f"%{val}%", f"%{val}%", f"%{val}%"))

#         rows = cur.fetchall()
#         cur.close()
#         conn.close()

#         self.patient_table.setRowCount(len(rows))
#         for row_i, row in enumerate(rows):
#             for col_i, col in enumerate(row):
#                 self.patient_table.setItem(row_i, col_i, QTableWidgetItem(str(col)))

#     # --------------------------------------------------------
#     # ADD / EDIT / DELETE PATIENT
#     # --------------------------------------------------------
#     def open_add_patient_window(self):
#         self.patient_window = PatientWindow()
#         self.patient_window.show()
#         self.patient_window.destroyed.connect(self.load_patients)

#     def edit_selected_patient(self):
#         row = self.patient_table.currentRow()
#         if row < 0:
#             QMessageBox.warning(self, "Error", "Please select a patient first.")
#             return

#         patient_id = self.patient_table.item(row, 0).text()
#         self.patient_window = PatientWindow(patient_id=patient_id)
#         self.patient_window.show()
#         self.patient_window.destroyed.connect(self.load_patients)

#     def delete_selected_patient(self):
#         row = self.patient_table.currentRow()
#         if row < 0:
#             QMessageBox.warning(self, "Error", "Please select a patient first.")
#             return

#         patient_id = self.patient_table.item(row, 0).text()

#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
#         conn.commit()
#         cur.close()
#         conn.close()

#         self.load_patients()


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from db_connection import get_connection

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QStackedWidget, QFrame, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer
from db_connection import get_connection
from patient_window import PatientWindow
from patient_detail_window import PatientDetailWindow  # new page
import csv
from appointment_list_window import AppointmentListPage


class DoctorDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Dental Clinic - Dr. {username}")
        self.setGeometry(200, 50, 1200, 700)
        self.setMinimumSize(2000, 1000)
        self.setStyleSheet("background-color: #f4f6fa;")

        self.doctor_id = self.get_doctor_id()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ------------------- LEFT PANEL -------------------
        left_panel = QFrame()
        left_panel.setFixedWidth(300)
        left_panel.setStyleSheet("""
            QFrame { background-color: #2f4050; }
            QLabel { color: white; font-size: 25px; padding-left: 15px; }
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 25px;
                padding: 12px;
                text-align: left;
                border: none;
            }
            QPushButton:hover { background-color: #3c5065; }
        """)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        title = QLabel(f"Dr. {username}")
        title.setStyleSheet("font-size: 35px; font-weight: bold;")
        left_layout.addWidget(title)
        left_layout.addSpacing(20)

        # Menu Buttons
        btn_patients = QPushButton("🧑‍⚕️  Patients")
        btn_appointments = QPushButton("📅  Appointments")
        left_layout.addWidget(btn_patients)
        left_layout.addWidget(btn_appointments)
        left_layout.addStretch()

        # ------------------- STACK -------------------
        self.stack = QStackedWidget()
        self.patient_page = self.create_patient_page()
        self.stack.addWidget(self.patient_page)
        self.appointment_page = AppointmentListPage(self.doctor_id)

        self.stack.addWidget(self.patient_page)
        self.stack.addWidget(self.appointment_page)

        # Add to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.stack)




        # Appointment page left as-is
        # self.appointment_page = AppointmentListPage(self.doctor_id)
        # self.stack.addWidget(self.appointment_page)
        btn_appointments.clicked.connect(self.show_appointments)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.stack)

        btn_patients.clicked.connect(lambda: self.stack.setCurrentWidget(self.patient_page))
        # btn_appointments.clicked.connect(lambda: QMessageBox.information(self, "Info", "Appointments page coming soon"))

    # ------------------- DOCTOR ID -------------------
    def get_doctor_id(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM doctors WHERE username=%s", (self.username,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else None


    def show_appointments(self):
        self.stack.setCurrentWidget(self.appointment_page)


    # ------------------- PATIENT PAGE -------------------
    def create_patient_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Search Box
        self.patient_search = QLineEdit()
        self.patient_search.setPlaceholderText("Search patient by name, phone, or email...")
        self.patient_search.textChanged.connect(self.filter_patients)
        layout.addWidget(self.patient_search)

        # Table Container
        table_container = QFrame()
        table_container.setStyleSheet("background-color: white; border-radius: 20px; padding: 15px;")
        table_layout = QVBoxLayout(table_container)

        # Patient Table
        self.patient_table = QTableWidget()
        self.patient_table.setColumnCount(6)
        self.patient_table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Email", "Age", "Created"])
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.patient_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.patient_table.cellDoubleClicked.connect(self.open_patient_detail)
        self.patient_table.setMinimumWidth(1000)
        self.patient_table.setMinimumHeight(1000)

        self.patient_table.horizontalHeader().setFixedHeight(80)   # Bigger header
        self.patient_table.verticalHeader().setDefaultSectionSize(40) 

        table_layout.addWidget(self.patient_table)
        layout.addWidget(table_container)

        # Buttons Row
        btn_row = QHBoxLayout()
        btn_add = QPushButton("➕  Add Patient")
        btn_edit = QPushButton("✏️  Edit")
        btn_delete = QPushButton("🗑️  Delete")
        btn_export = QPushButton("🖨️  Print / Export All")
        for btn in [btn_add, btn_edit, btn_delete, btn_export]:
            btn.setStyleSheet("background-color: #2b7cff; color: white; padding: 10px; font-size: 25px; border-radius: 10px;")
            btn_row.addWidget(btn)

        btn_add.clicked.connect(self.open_add_patient_window)
        btn_edit.clicked.connect(self.edit_selected_patient)
        btn_delete.clicked.connect(self.delete_selected_patient)
        # btn_export.clicked.connect(self.export_all_patients)
        btn_export.clicked.connect(self.export_patients_pdf)

        layout.addLayout(btn_row)

        page.setLayout(layout)
        self.load_patients()
        return page

    # ------------------- LOAD / FILTER -------------------
    def load_patients(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, phone_number, email, age, created_at FROM patients ORDER BY id DESC;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_patients)
        self.timer.start(1000) 
        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.patient_table.setRowCount(len(rows))
        for row_i, row in enumerate(rows):
            for col_i, col in enumerate(row):
                self.patient_table.setItem(row_i, col_i, QTableWidgetItem(str(col)))

    def filter_patients(self):
        val = self.patient_search.text()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, phone_number, email, age, created_at
            FROM patients
            WHERE name ILIKE %s OR phone_number ILIKE %s OR email ILIKE %s
            ORDER BY id DESC;
        """, (f"%{val}%", f"%{val}%", f"%{val}%"))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.patient_table.setRowCount(len(rows))
        for row_i, row in enumerate(rows):
            for col_i, col in enumerate(row):
                self.patient_table.setItem(row_i, col_i, QTableWidgetItem(str(col)))

    # ------------------- ADD / EDIT / DELETE -------------------
    def open_add_patient_window(self):
        self.patient_window = PatientWindow()
        self.patient_window.show()
        self.patient_window.destroyed.connect(self.load_patients)

    def edit_selected_patient(self):
        row = self.patient_table.currentRow()
        if row < 0: return QMessageBox.warning(self, "Error", "Select a patient first.")
        patient_id = self.patient_table.item(row, 0).text()
        self.patient_window = PatientWindow(patient_id=patient_id)
        self.patient_window.show()
        self.patient_window.destroyed.connect(self.load_patients)

    def delete_selected_patient(self):
        row = self.patient_table.currentRow()
        if row < 0: return QMessageBox.warning(self, "Error", "Select a patient first.")
        patient_id = self.patient_table.item(row, 0).text()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        conn.commit()
        cur.close()
        conn.close()
        self.load_patients()

    # ------------------- OPEN PATIENT DETAIL -------------------
    def open_patient_detail(self, row, column):
        patient_id = int(self.patient_table.item(row, 0).text())
        self.detail_window = PatientDetailWindow(patient_id)
        self.detail_window.show()

    # ------------------- EXPORT ALL PATIENTS -------------------
    # def export_patients_pdf(self):
    #     path, _ = QFileDialog.getSaveFileName(self, "Export All Patients", "", "PDF Files (*.pdf)")
    #     if not path:
    #         return

    #     conn = get_connection()
    #     cur = conn.cursor()
    #     cur.execute("SELECT id, name, phone_number, email, age, created_at FROM patients ORDER BY id;")
    #     patients = cur.fetchall()

    #     all_data = []
    #     headers = ["ID","Name","Phone","Email","Age","Created","Appt Date","Appt Time","Doctor","Notes"]
    #     all_data.append(headers)

    #     for p in patients:
    #         patient_id = p[0]
    #         cur.execute("SELECT date, time, doctor_name, notes FROM appointments WHERE patient_id=%s ORDER BY date;", (patient_id,))
    #         appointments = cur.fetchall()
    #         if appointments:
    #             for a in appointments:
    #                 all_data.append(list(p) + list(a))
    #         else:
    #             all_data.append(list(p) + ["", "", "", ""])

    #     cur.close()
    #     conn.close()

    #     # Create PDF
    #     pdf = SimpleDocTemplate(path, pagesize=A4)
    #     styles = getSampleStyleSheet()
    #     elements = []

    #     title = Paragraph("Dental Clinic - Patients Report", styles['Title'])
    #     elements.append(title)
    #     elements.append(Spacer(1, 12))

    #     table = Table(all_data, repeatRows=1)
    #     table.setStyle(TableStyle([
    #         ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2b7cff')),  # header bg color
    #         ('TEXTCOLOR', (0,0), (-1,0), colors.white),                # header text color
    #         ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    #         ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    #         ('FONTSIZE', (0,0), (-1,0), 12),
    #         ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    #         ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightgrey])
    #     ]))

    #     elements.append(table)
    #     pdf.build(elements)

    #     QMessageBox.information(self, "Success", f"All patients and appointments exported to PDF:\n{path}")



    def export_patients_pdf(self):
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from datetime import datetime

        path, _ = QFileDialog.getSaveFileName(self, "Export All Patients", "", "PDF Files (*.pdf)")
        if not path:
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, phone_number, email, age, address, created_at FROM patients ORDER BY id;")
        patients = cur.fetchall()

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.textColor = colors.HexColor("#1A4A9E")

        header_style = ParagraphStyle(
            "header",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#1A4A9E"),
            spaceAfter=12
        )

        normal = styles["BodyText"]

        pdf = SimpleDocTemplate(
            path,
            pagesize=A4,
            rightMargin=25,
            leftMargin=25,
            topMargin=40,
            bottomMargin=25
        )

        elements = []

        # -----------------------------
        # PDF HEADER
        # -----------------------------
        elements.append(Paragraph("🦷 Dental Clinic – Full Patient Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d  %H:%M')}", normal))
        elements.append(Spacer(1, 12))

        # -----------------------------
        # START PATIENT EXPORT
        # -----------------------------
        for p in patients:
            patient_id, name, phone, email, age, address, created_at = p

            # Patient card header
            elements.append(Paragraph(f"<b>Patient ID:</b> {patient_id}", header_style))

            # Patient general info table
            info_data = [
                ["Name:", name],
                ["Phone:", phone],
                ["Email:", email],
                ["Age:", str(age)],
                ["Address:", address],
                ["Registered On:", str(created_at)]
            ]

            info_table = Table(info_data, colWidths=[4*cm, 12*cm])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#E9F0FF")),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.grey),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(info_table)
            elements.append(Spacer(1, 12))

            # -----------------------------
            # FETCH APPOINTMENTS
            # -----------------------------
            cur.execute("""
                SELECT date, time, doctor_name, treatment, notes 
                FROM appointments 
                WHERE patient_id=%s ORDER BY date;
            """, (patient_id,))
            appointments = cur.fetchall()

            elements.append(Paragraph("Appointments", header_style))

            if appointments:
                appt_table_data = [
                    ["Date", "Time", "Doctor", "Treatment", "Notes"]
                ]

                for a in appointments:
                    appt_table_data.append(list(map(str, a)))

                appt_table = Table(appt_table_data, colWidths=[3*cm, 2.5*cm, 4*cm, 4*cm, 5*cm])
                appt_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A4A9E")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]))

                elements.append(appt_table)

            else:
                elements.append(Paragraph("No appointments found.", normal))

            elements.append(Spacer(1, 20))
            elements.append(PageBreak())

        cur.close()
        conn.close()

        pdf.build(elements)

        QMessageBox.information(self, "Success", f"Full report exported beautifully:\n{path}")
