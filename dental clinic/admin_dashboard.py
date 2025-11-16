
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QApplication
from patient_window import PatientWindow
from appointment_window import AppointmentWindow
from doctor_window import DoctorWindow

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dental Clinic - Admin Dashboard")

        # -------- MAKE WINDOW HALF OF THE SCREEN --------
        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()

        window_width = screen_width // 2
        window_height = screen_height // 2

        # Center on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.setGeometry(x, y, window_width, window_height)
        # ------------------------------------------------

        # ---- UI ----
        QLabel("Welcome, Admin!", self).move(window_width // 2 - 60, 40)

        btn_doctor = QPushButton("Manage Doctors", self)
        btn_doctor.move(window_width // 2 - 80, 100)
        btn_doctor.clicked.connect(self.open_doctor_window)

        btn_patient = QPushButton("Manage Patients", self)
        btn_patient.move(window_width // 2 - 80, 160)
        btn_patient.clicked.connect(self.open_patient_window)

        btn_appointment = QPushButton("Manage Appointments", self)
        btn_appointment.move(window_width // 2 - 80, 220)
        btn_appointment.clicked.connect(self.open_appointment_window)

    def open_doctor_window(self):
        self.doctor_window = DoctorWindow()
        self.doctor_window.show()

    def open_patient_window(self):
        self.patient_window = PatientWindow()
        self.patient_window.show()

    def open_appointment_window(self):
        self.appointment_window = AppointmentWindow()
        self.appointment_window.show()
