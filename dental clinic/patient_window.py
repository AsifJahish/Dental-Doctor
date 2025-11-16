from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout
from db_connection import get_connection

class PatientWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Management")
        self.setGeometry(300, 100, 600, 600)

        layout = QGridLayout()

        self.name = QLineEdit()
        self.age = QLineEdit()
        self.contact = QLineEdit()
        self.address = QLineEdit()

        layout.addWidget(QLabel("Name:"), 0, 0)
        layout.addWidget(self.name, 0, 1)
        layout.addWidget(QLabel("Age:"), 1, 0)
        layout.addWidget(self.age, 1, 1)
        layout.addWidget(QLabel("Contact:"), 2, 0)
        layout.addWidget(self.contact, 2, 1)
        layout.addWidget(QLabel("Address:"), 3, 0)
        layout.addWidget(self.address, 3, 1)

        self.teeth_fields = {}
        tooth_labels = ["Upper Left", "Upper Right", "Lower Left", "Lower Right"]
        positions = [4, 11, 18, 25]

        for i, label in enumerate(tooth_labels):
            layout.addWidget(QLabel(label), positions[i], 0)
            for t in range(1, 8):
                key = f"{label.lower().replace(' ', '_')}_{t}"
                self.teeth_fields[key] = QLineEdit()
                layout.addWidget(QLabel(str(t)), positions[i], t)
                layout.addWidget(self.teeth_fields[key], positions[i] + 1, t)

        save_btn = QPushButton("Save Patient")
        save_btn.clicked.connect(self.save_patient)
        layout.addWidget(save_btn, 35, 1)
        self.setLayout(layout)

    def save_patient(self):
        conn = get_connection()
        cur = conn.cursor()

        fields = {
            "name": self.name.text(),
            "age": self.age.text(),
            "contact": self.contact.text(),
            "address": self.address.text(),
        }

        for key, val in self.teeth_fields.items():
            fields[key] = val.text()

        columns = ', '.join(fields.keys())
        values = tuple(fields.values())
        placeholders = ', '.join(['%s'] * len(fields))

        cur.execute(f"INSERT INTO patients ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        QMessageBox.information(self, "Success", "Patient added successfully.")
        cur.close()
        conn.close()

