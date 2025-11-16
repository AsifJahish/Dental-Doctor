from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
from db_connection import get_connection
import bcrypt

class DoctorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Doctors")
        self.setGeometry(400, 200, 400, 300)

        layout = QGridLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.full_name = QLineEdit()
        self.specialization = QLineEdit()

        layout.addWidget(QLabel("Username:"), 0, 0)
        layout.addWidget(self.username, 0, 1)
        layout.addWidget(QLabel("Password:"), 1, 0)
        layout.addWidget(self.password, 1, 1)
        layout.addWidget(QLabel("Full Name:"), 2, 0)
        layout.addWidget(self.full_name, 2, 1)
        layout.addWidget(QLabel("Specialization:"), 3, 0)
        layout.addWidget(self.specialization, 3, 1)

        btn_add = QPushButton("Add Doctor")
        btn_add.clicked.connect(self.add_doctor)
        layout.addWidget(btn_add, 5, 1)

        self.setLayout(layout)

    def add_doctor(self):
        conn = get_connection()
        cur = conn.cursor()

        hashed_pw = bcrypt.hashpw(self.password.text().encode(), bcrypt.gensalt())

        cur.execute("""
            INSERT INTO doctors (username, password, full_name, specialization)
            VALUES (%s, %s, %s, %s)
        """, (self.username.text(), hashed_pw.decode(), self.full_name.text(), self.specialization.text()))

        conn.commit()
        QMessageBox.information(self, "Success", "Doctor added successfully.")
        cur.close()
        conn.close()
