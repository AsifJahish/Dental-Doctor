from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
from db_connection import get_connection

class AppointmentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Appointment Management")
        self.setGeometry(400, 200, 400, 300)

        layout = QGridLayout()

        self.patient_id = QLineEdit()
        self.date = QLineEdit()
        self.time = QLineEdit()
        self.treatment = QLineEdit()

        layout.addWidget(QLabel("Patient ID:"), 0, 0)
        layout.addWidget(self.patient_id, 0, 1)
        layout.addWidget(QLabel("Date (YYYY-MM-DD):"), 1, 0)
        layout.addWidget(self.date, 1, 1)
        layout.addWidget(QLabel("Time (HH:MM):"), 2, 0)
        layout.addWidget(self.time, 2, 1)
        layout.addWidget(QLabel("Treatment:"), 3, 0)
        layout.addWidget(self.treatment, 3, 1)

        btn = QPushButton("Save Appointment")
        btn.clicked.connect(self.save_appointment)
        layout.addWidget(btn, 5, 1)

        self.setLayout(layout)

    def save_appointment(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO appointments (patient_id, date, time, treatment) VALUES (%s, %s, %s, %s)",
            (self.patient_id.text(), self.date.text(), self.time.text(), self.treatment.text())
        )
        conn.commit()
        QMessageBox.information(self, "Success", "Appointment saved.")
        cur.close()
        conn.close()
