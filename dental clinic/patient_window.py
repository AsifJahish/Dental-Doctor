
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, 
    QGridLayout, QFileDialog, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from db_connection import get_connection


class PatientWindow(QWidget):
    def __init__(self, patient_id=None):
        super().__init__()
        self.patient_id = patient_id
        self.teeth_image_path = None

        self.setWindowTitle("Patient Management")
        self.setGeometry(200, 50, 1100, 1000)
        self.setMinimumSize(1500, 1500)

        self.setStyleSheet("""
            QWidget { font-size: 30px; background-color: #f7f9fc; }
            QLineEdit { padding: 8px; border-radius: 6px; border: 1px solid #c7c7c7; background: white; }
            QPushButton { background-color: #0078ff; color: white; border-radius: 6px; padding: 10px; }
            QPushButton:hover { background-color: #005fcc; }
            QLabel { font-weight: bold; }
        """)

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

        regex = QRegExp(r'^\+?[0-9]{7,15}$')
        self.phone.setValidator(QRegExpValidator(regex))

        row = 0
        for label, widget in [("Name:", self.name), ("Age:", self.age),
                              ("Phone:", self.phone), ("Email:", self.email),
                              ("Address:", self.address)]:
            form_layout.addWidget(QLabel(label), row, 0)
            form_layout.addWidget(widget, row, 1)
            row += 1

        # -------------------------
        # PAYMENT FIELDS
        # -------------------------
        self.total_amount = QLineEdit()
        self.paid_amount = QLineEdit()
        self.discount_percent = QLineEdit()
        self.remaining_amount = QLineEdit()
        self.remaining_amount.setReadOnly(True)
        self.remaining_amount.setStyleSheet("background: #e8e8e8;")

        # Connect signals
        for widget in [self.total_amount, self.paid_amount, self.discount_percent]:
            widget.textChanged.connect(self.update_remaining)

        for label, widget in [("Total Amount:", self.total_amount),
                              ("Paid Amount:", self.paid_amount),
                              ("Discount %:", self.discount_percent),
                              ("Remaining Amount:", self.remaining_amount)]:
            form_layout.addWidget(QLabel(label), row, 0)
            form_layout.addWidget(widget, row, 1)
            row += 1

        # -------------------------
        # IMAGE UPLOAD
        # -------------------------
        form_layout.addWidget(QLabel("Teeth Image:"), row, 0)
        img_box = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 200)
        self.image_label.setStyleSheet("border: 1px solid gray; border-radius: 8px;")
        btn_upload = QPushButton("Upload Image")
        btn_upload.clicked.connect(self.upload_teeth_image)
        img_box.addWidget(self.image_label)
        img_box.addWidget(btn_upload)
        form_layout.addLayout(img_box, row, 1)
        row += 1

        # -------------------------
        # TEETH CHART
        # -------------------------
        form_layout.addWidget(QLabel("Teeth Chart:"), row, 0)
        row += 1

        self.teeth_buttons = {}
        teeth_grid = QGridLayout()
        quadrants = ['upper_left', 'upper_right', 'lower_left', 'lower_right']
        quadrant_labels = ["Upper Left", "Upper Right", "Lower Left", "Lower Right"]

        for q_index, quadrant in enumerate(quadrants):
            teeth_grid.addWidget(QLabel(quadrant_labels[q_index]), q_index, 0)
            for i in range(1, 8):
                tooth_name = f"{quadrant}_{i}"
                btn = QPushButton(str(i))
                btn.setCheckable(True)
                btn.setFixedSize(40, 40)
                btn.setStyleSheet("""
                    QPushButton { background-color: white; border-radius: 6px; border: 1px solid #666; }
                    QPushButton:checked { background-color: #00aaff; color: white; }
                """)
                self.teeth_buttons[tooth_name] = btn
                teeth_grid.addWidget(btn, q_index, i)

        form_layout.addLayout(teeth_grid, row, 0, 1, 2)
        row += 1

        layout.addLayout(form_layout)

        # -------------------------
        # SAVE BUTTON
        # -------------------------
        save_btn = QPushButton("Save Patient")
        save_btn.setFixedHeight(45)
        save_btn.clicked.connect(self.save_patient)
        layout.addWidget(save_btn)

        self.setLayout(layout)
        if self.patient_id:
            self.load_patient()

    # ---------------------------------------------------
    # CALCULATE REMAINING AMOUNT WITH DISCOUNT
    # ---------------------------------------------------
    def update_remaining(self):
        try:
            total = float(self.total_amount.text() or 0)
            discount = float(self.discount_percent.text() or 0)
            paid = float(self.paid_amount.text() or 0)
            discounted_total = total - (total * discount / 100)
            remaining = discounted_total - paid
            self.remaining_amount.setText(str(round(remaining, 2)))
        except:
            self.remaining_amount.setText("0")

    # ---------------------------------------------------
    # IMAGE UPLOAD
    # ---------------------------------------------------
    def upload_teeth_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Teeth Image", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if path:
            self.teeth_image_path = path
            self.image_label.setPixmap(QPixmap(path).scaled(200, 200, Qt.KeepAspectRatio))

    # ---------------------------------------------------
    # LOAD PATIENT
    # ---------------------------------------------------
    def load_patient(self):
        conn = get_connection()
        cur = conn.cursor()

        teeth_columns = ", ".join(self.teeth_buttons.keys())
        cur.execute(f"""
            SELECT name, age, phone_number, email, address, 
                   total_amount, paid_amount, discount_percent, remaining_amount,
                   photo_path, {teeth_columns}
            FROM patients
            WHERE id = %s
        """, (self.patient_id,))

        data = cur.fetchone()
        cur.close()
        conn.close()
        if not data: return

        self.name.setText(data[0])
        self.age.setText(str(data[1]))
        self.phone.setText(data[2])
        self.email.setText(data[3])
        self.address.setText(data[4])
        self.total_amount.setText(str(data[5]))
        self.paid_amount.setText(str(data[6]))
        self.discount_percent.setText(str(data[7]))
        self.remaining_amount.setText(str(data[8]))

        if data[9]:
            self.teeth_image_path = data[9]
            self.image_label.setPixmap(QPixmap(data[9]).scaled(200, 200, Qt.KeepAspectRatio))

        for i, tooth_name in enumerate(self.teeth_buttons.keys()):
            self.teeth_buttons[tooth_name].setChecked(data[10 + i])

    # ---------------------------------------------------
    # SAVE PATIENT
    # ---------------------------------------------------
    def save_patient(self):
        conn = get_connection()
        cur = conn.cursor()

        teeth_columns = list(self.teeth_buttons.keys())
        teeth_values = [self.teeth_buttons[t].isChecked() for t in teeth_columns]

        total = float(self.total_amount.text() or 0)
        paid = float(self.paid_amount.text() or 0)
        discount = float(self.discount_percent.text() or 0)
        remaining = total - (total * discount / 100) - paid

        if self.patient_id:
            columns_set = ", ".join([f"{c}=%s" for c in teeth_columns])
            cur.execute(f"""
                UPDATE patients
                SET name=%s, age=%s, phone_number=%s, email=%s, address=%s,
                    total_amount=%s, paid_amount=%s, discount_percent=%s, remaining_amount=%s,
                    photo_path=%s, {columns_set}
                WHERE id=%s
            """, (
                self.name.text(), self.age.text(), self.phone.text(),
                self.email.text(), self.address.text(),
                total, paid, discount, remaining,
                self.teeth_image_path,
                *teeth_values,
                self.patient_id
            ))
        else:
            columns = ["name", "age", "phone_number", "email", "address",
                       "total_amount", "paid_amount", "discount_percent", "remaining_amount",
                       "photo_path"] + teeth_columns
            placeholders = ",".join(["%s"] * len(columns))
            cur.execute(f"""
                INSERT INTO patients ({",".join(columns)})
                VALUES ({placeholders})
            """, (
                self.name.text(), self.age.text(), self.phone.text(),
                self.email.text(), self.address.text(),
                total, paid, discount, remaining,
                self.teeth_image_path,
                *teeth_values
            ))

        conn.commit()
        cur.close()
        conn.close()
        QMessageBox.information(self, "Success", "Patient saved successfully.")
        self.close()
