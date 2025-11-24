from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
    QGridLayout, QDateEdit, QTimeEdit, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import QDate, QTime, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from db_connection import get_connection


class AppointmentWindow(QWidget):
    def __init__(self, doctor_id, appointment_id=None):
        super().__init__()
        self.doctor_id = doctor_id
        self.appointment_id = appointment_id   # <-- NEW

        # Half-screen window
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(
            screen.width() // 4,
            screen.height() // 4,
            screen.width() // 2,
            screen.height() // 2
        )

        # Title changes depending on mode
        if self.appointment_id:
            self.setWindowTitle("Edit Appointment")
        else:
            self.setWindowTitle("Create Appointment")

        # =========================
        #     UI SETUP (same as before)
        # =========================
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        title = QLabel("Edit Appointment" if appointment_id else "Create New Appointment")
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(25)
        form_layout.setHorizontalSpacing(20)

        font_input = "padding: 12px; font-size: 18px;"

        # Inputs
        self.patient_id = QLineEdit()
        self.patient_id.setStyleSheet(font_input)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setStyleSheet(font_input)

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setStyleSheet(font_input)

        self.treatment = QLineEdit()
        self.treatment.setStyleSheet(font_input)

        # Add to form
        form_layout.addWidget(self.make_label("Patient ID:"), 0, 0)
        form_layout.addWidget(self.patient_id, 0, 1)

        form_layout.addWidget(self.make_label("Select Date:"), 1, 0)
        form_layout.addWidget(self.date_edit, 1, 1)

        form_layout.addWidget(self.make_label("Select Time:"), 2, 0)
        form_layout.addWidget(self.time_edit, 2, 1)

        form_layout.addWidget(self.make_label("Treatment:"), 3, 0)
        form_layout.addWidget(self.treatment, 3, 1)

        main_layout.addLayout(form_layout)

        # Save button
        btn = QPushButton("Update Appointment" if appointment_id else "Save Appointment")
        btn.setFont(QFont("Arial", 18, QFont.Bold))
        btn.clicked.connect(self.save_appointment)
        main_layout.addWidget(btn)

        self.setLayout(main_layout)

        # Load existing appointment details if editing
        if self.appointment_id:
            self.load_existing_appointment()


    def load_existing_appointment(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT patient_id, date, time, treatment
            FROM appointments
            WHERE id = %s
        """, (self.appointment_id,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            self.patient_id.setText(str(row[0]))
            self.date_edit.setDate(QDate.fromString(str(row[1]), "yyyy-MM-dd"))
            self.time_edit.setTime(QTime.fromString(str(row[2]), "HH:mm"))
            self.treatment.setText(row[3])


    # Helper to create styled labels
    def make_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Arial", 18, QFont.Bold))
        return label

    # ================================
    #       SAVE APPOINTMENT
    # ================================
    def save_appointment(self):
            conn = get_connection()
            cur = conn.cursor()

            date_string = self.date_edit.date().toString("yyyy-MM-dd")
            time_string = self.time_edit.time().toString("HH:mm")

            if self.appointment_id:
                # UPDATE
                cur.execute("""
                    UPDATE appointments
                    SET patient_id = %s, date = %s, time = %s, treatment = %s
                    WHERE id = %s
                """, (
                    int(self.patient_id.text()),
                    date_string,
                    time_string,
                    self.treatment.text(),
                    int(self.appointment_id)
                ))

                QMessageBox.information(self, "Updated", "Appointment updated successfully.")

            else:
                # INSERT
                cur.execute("""
                    INSERT INTO appointments (patient_id, doctor_id, date, time, treatment)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    int(self.patient_id.text()),
                    int(self.doctor_id),
                    date_string,
                    time_string,
                    self.treatment.text()
                ))

                QMessageBox.information(self, "Success", "Appointment created successfully.")

                



            conn.commit()
            cur.close()
            conn.close()
            self.close()
