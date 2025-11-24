from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, 
    QGridLayout, QFileDialog, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
import json
from db_connection import get_connection


class PatientWindow(QWidget):
    def __init__(self, patient_id=None):
        super().__init__()
        self.patient_id = patient_id   # For edit mode
        self.teeth_image_path = None

        self.setWindowTitle("Patient Management")
        self.setGeometry(300, 100, 1000, 900)

        layout = QVBoxLayout()
        form_layout = QGridLayout()

        # -------------------------
        # BASIC FIELDS
        # -------------------------
        self.name = QLineEdit()
        self.age = QLineEdit()
        self.phone = QLineEdit()
        self.email = QLineEdit()
        self.address = QLineEdit()

        # phone number validation
        regex = QRegExp(r'^\+?[0-9]{7,15}$')
        self.phone.setValidator(QRegExpValidator(regex))

        row = 0
        form_layout.addWidget(QLabel("Name:"), row, 0)
        form_layout.addWidget(self.name, row, 1); row += 1

        form_layout.addWidget(QLabel("Age:"), row, 0)
        form_layout.addWidget(self.age, row, 1); row += 1

        form_layout.addWidget(QLabel("Phone:"), row, 0)
        form_layout.addWidget(self.phone, row, 1); row += 1

        form_layout.addWidget(QLabel("Email:"), row, 0)
        form_layout.addWidget(self.email, row, 1); row += 1

        form_layout.addWidget(QLabel("Address:"), row, 0)
        form_layout.addWidget(self.address, row, 1); row += 1

        # -------------------------
        # TEETH IMAGE UPLOAD
        # -------------------------
        form_layout.addWidget(QLabel("Teeth Image:"), row, 0)

        img_box = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 200)
        self.image_label.setStyleSheet("border: 1px solid gray;")

        btn_upload = QPushButton("Upload Image")
        btn_upload.clicked.connect(self.upload_teeth_image)

        img_box.addWidget(self.image_label)
        img_box.addWidget(btn_upload)

        form_layout.addLayout(img_box, row, 1)
        row += 1

        # -------------------------
        # TEETH CHART BUTTONS
        # -------------------------
        form_layout.addWidget(QLabel("Teeth Chart:"), row, 0)
        row += 1

        self.teeth_buttons = {}  # { 'upper_left_1': QPushButton, ... }
        teeth_grid = QGridLayout()

        quadrants = ['upper_left', 'upper_right', 'lower_left', 'lower_right']
        for q_index, quadrant in enumerate(quadrants):
            for i in range(1, 8):  # 1 to 7
                tooth_name = f"{quadrant}_{i}"
                btn = QPushButton(str(i))
                btn.setCheckable(True)
                btn.setFixedSize(40, 40)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        border: 1px solid #444;
                    }
                    QPushButton:checked {
                        background-color: #00bfff;
                    }
                """)
                self.teeth_buttons[tooth_name] = btn
                teeth_grid.addWidget(btn, q_index, i-1)

        form_layout.addLayout(teeth_grid, row, 0, 1, 2)
        row += 1

        layout.addLayout(form_layout)

        # -------------------------
        # SAVE BUTTON
        # -------------------------
        save_btn = QPushButton("Save Patient")
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self.save_patient)
        layout.addWidget(save_btn)

        self.setLayout(layout)

        # Load patient (edit mode)
        if self.patient_id:
            self.load_patient()


    # ===================================================
    # IMAGE UPLOAD
    # ===================================================
    def upload_teeth_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Teeth Image", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if path:
            self.teeth_image_path = path
            self.image_label.setPixmap(QPixmap(path).scaled(
                200, 200, Qt.KeepAspectRatio
            ))


    # ===================================================
    # LOAD PATIENT (EDIT MODE)
    # ===================================================
    def load_patient(self):
        conn = get_connection()
        cur = conn.cursor()

        # get all teeth columns + basic info
        teeth_columns = ", ".join(self.teeth_buttons.keys())
        cur.execute(f"""
            SELECT name, age, phone_number, email, address, photo_path, {teeth_columns}
            FROM patients
            WHERE id = %s
        """, (self.patient_id,))

        data = cur.fetchone()
        cur.close()
        conn.close()

        if not data:
            return

        self.name.setText(data[0])
        self.age.setText(str(data[1]))
        self.phone.setText(data[2])
        self.email.setText(data[3])
        self.address.setText(data[4])

        # image
        if data[5]:
            self.teeth_image_path = data[5]
            self.image_label.setPixmap(QPixmap(data[5]).scaled(200, 200, Qt.KeepAspectRatio))

        # teeth chart state
        for i, tooth_name in enumerate(self.teeth_buttons.keys()):
            self.teeth_buttons[tooth_name].setChecked(data[6 + i])


    # ===================================================
    # SAVE PATIENT
    # ===================================================
    def save_patient(self):
        conn = get_connection()
        cur = conn.cursor()

        teeth_columns = list(self.teeth_buttons.keys())
        teeth_values = [self.teeth_buttons[t].isChecked() for t in teeth_columns]

        if self.patient_id:  # update mode
            columns_set = ", ".join([f"{c}=%s" for c in teeth_columns])
            cur.execute(f"""
                UPDATE patients
                SET name=%s, age=%s, phone_number=%s, email=%s, address=%s,
                    photo_path=%s, {columns_set}
                WHERE id=%s
            """, (
                self.name.text(),
                self.age.text(),
                self.phone.text(),
                self.email.text(),
                self.address.text(),
                self.teeth_image_path,
                *teeth_values,
                self.patient_id
            ))
        else:  # insert new
            columns = ["name","age","phone_number","email","address","photo_path"] + teeth_columns
            placeholders = ",".join(["%s"] * len(columns))
            cur.execute(f"""
                INSERT INTO patients ({",".join(columns)})
                VALUES ({placeholders})
            """, (
                self.name.text(),
                self.age.text(),
                self.phone.text(),
                self.email.text(),
                self.address.text(),
                self.teeth_image_path,
                *teeth_values
            ))

        conn.commit()
        cur.close()
        conn.close()

        QMessageBox.information(self, "Success", "Patient saved successfully.")
        self.close()
