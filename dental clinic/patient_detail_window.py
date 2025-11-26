from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QScrollArea
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from db_connection import get_connection
import webbrowser
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class PatientDetailWindow(QWidget):
    def __init__(self, patient_id):
        super().__init__()
        self.patient_id = patient_id
        self.teeth_image_path = None
        self.patient_data = None

        self.setWindowTitle("Patient Full Details")
        self.setGeometry(50, 50, 1300, 900)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll.setWidget(scroll_content)
        main_layout = QVBoxLayout(scroll_content)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("🦷 Patient Details & Appointment History")
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(title)

        # Patient Info Frame
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: #f7f9fc;
                padding: 25px;
                border-radius: 15px;
                border: 2px solid #d0d0d0;
            }
        """)
        info_layout = QHBoxLayout(info_frame)
        info_layout.setSpacing(30)

        # Left Column: Text Info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(10)
        self.lbl_name = QLabel()
        self.lbl_age = QLabel()
        self.lbl_phone = QLabel()
        self.lbl_email = QLabel()
        self.lbl_address = QLabel()
        self.lbl_total_amount = QLabel()
        self.lbl_paid_amount = QLabel()
        self.lbl_discount = QLabel()
        self.lbl_remaining = QLabel()

        for lbl in [self.lbl_name, self.lbl_age, self.lbl_phone, self.lbl_email,
                    self.lbl_address, self.lbl_total_amount, self.lbl_paid_amount,
                    self.lbl_discount, self.lbl_remaining]:
            lbl.setFont(QFont("Arial", 15))
            lbl.setStyleSheet("color: #34495e;")
            text_layout.addWidget(lbl)

        info_layout.addLayout(text_layout)

        # Right Column: Teeth Image
        self.image_label = QLabel()
        self.image_label.setFixedSize(350, 350)
        self.image_label.setStyleSheet(
            "border: 2px solid #bdc3c7; border-radius: 10px; background: #ecf0f1;"
        )
        info_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        main_layout.addWidget(info_frame)

        # Appointment Table
        appt_title = QLabel("📅 Appointment History")
        appt_title.setFont(QFont("Arial", 20, QFont.Bold))
        appt_title.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(appt_title)

        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(4)
        self.appointment_table.setHorizontalHeaderLabels(["Date", "Time", "Doctor", "Notes"])
        self.appointment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.appointment_table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1px solid #ccc;
                gridline-color: #bdc3c7;
            }
            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
        """)
        self.appointment_table.setMinimumHeight(300)
        main_layout.addWidget(self.appointment_table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_pdf = QPushButton("📄 Export PDF")
        self.btn_pdf.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white; 
                padding: 12px 20px; 
                font-size: 16px; 
                border-radius: 8px;
            }
            QPushButton:hover {background-color: #2ecc71;}
        """)
        self.btn_pdf.clicked.connect(self.print_pdf)



        btn_layout.addWidget(self.btn_pdf)

        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # Scrollable window
        window_layout = QVBoxLayout(self)
        window_layout.addWidget(scroll)

        # Load data
        self.load_patient_info()
        self.load_appointments()

    # Load patient info
    def load_patient_info(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT name, age, phone_number, email, address,
                   total_amount, paid_amount, discount_percent,
                   remaining_amount, photo_path
            FROM patients
            WHERE id = %s
        """, (self.patient_id,))
        data = cur.fetchone()
        cur.close()
        conn.close()
        if not data:
            QMessageBox.warning(self, "Error", "Patient not found.")
            self.close()
            return

        self.patient_data = data
        self.lbl_name.setText(f"• Name: {data[0]}")
        self.lbl_age.setText(f"• Age: {data[1]}")
        self.lbl_phone.setText(f"• Phone: {data[2]}")
        self.lbl_email.setText(f"• Email: {data[3]}")
        self.lbl_address.setText(f"• Address: {data[4]}")
        self.lbl_total_amount.setText(f"• Total Amount: ${data[5]}")
        self.lbl_paid_amount.setText(f"• Paid Amount: ${data[6]}")
        self.lbl_discount.setText(f"• Discount (%): {data[7]}")
        self.lbl_remaining.setText(f"• Remaining Amount: ${data[8]}")

        self.teeth_image_path = data[9]
        if self.teeth_image_path:
            self.image_label.setPixmap(
                QPixmap(self.teeth_image_path).scaled(350, 350, Qt.KeepAspectRatio)
            )

    # Load appointments
    def load_appointments(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT date, time, doctor_name, notes
            FROM appointments
            WHERE patient_id = %s
            ORDER BY date
        """, (self.patient_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        self.appointment_table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.appointment_table.setItem(r, c, item)

    # Generate PDF


  
    def print_pdf(self):
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from datetime import datetime

        if not self.patient_data:
            QMessageBox.warning(self, "Error", "No patient data to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return

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
            file_path,
            pagesize=A4,
            rightMargin=25,
            leftMargin=25,
            topMargin=40,
            bottomMargin=25
        )

        elements = []

        # PDF Header
        elements.append(Paragraph("🦷 Dental Clinic – Patient Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d  %H:%M')}", normal))
        elements.append(Spacer(1, 12))

        # -----------------------------
        # Patient Info
        # -----------------------------
        labels = [
            ("Name:", self.patient_data[0]),
            ("Age:", str(self.patient_data[1])),
            ("Phone:", self.patient_data[2]),
            ("Email:", self.patient_data[3]),
            ("Address:", self.patient_data[4]),
            ("Total Amount:", f"${self.patient_data[5]}"),
            ("Paid Amount:", f"${self.patient_data[6]}"),
            ("Discount (%):", str(self.patient_data[7])),
            ("Remaining Amount:", f"${self.patient_data[8]}")
        ]

        info_table = Table(labels, colWidths=[5*cm, 10*cm])
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
        # Teeth Image
        # -----------------------------
        if self.teeth_image_path:
            elements.append(Paragraph("Teeth Image:", header_style))
            elements.append(Spacer(1, 6))
            elements.append(Image(self.teeth_image_path, width=8*cm, height=8*cm))
            elements.append(Spacer(1, 12))

        # -----------------------------
        # Appointment History
        # -----------------------------
        elements.append(Paragraph("Appointment History", header_style))

        if self.appointment_table.rowCount() > 0:
            appt_data = [["Date", "Time", "Doctor", "Notes"]]
            for r in range(self.appointment_table.rowCount()):
                row = [self.appointment_table.item(r, c).text() for c in range(4)]
                appt_data.append(row)

            appt_table = Table(appt_data, colWidths=[3*cm, 3*cm, 5*cm, 7*cm])
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

        # Build PDF
        try:
            pdf.build(elements)
            QMessageBox.information(self, "Success", "PDF created successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"PDF error: {e}")
