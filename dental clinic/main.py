from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from login_window import LoginWindow
from doctor_login_window import DoctorLoginWindow
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dental Clinic - Choose Role")

        # -------- MAKE WINDOW HALF OF SCREEN --------
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

        # Buttons centered relative to new window size
        btn_x = window_width // 2 - 60

        admin_btn = QPushButton("Admin Login", self)
        admin_btn.move(btn_x, 100)
        admin_btn.clicked.connect(self.open_admin_login)

        doctor_btn = QPushButton("Doctor Login", self)
        doctor_btn.move(btn_x, 180)
        doctor_btn.clicked.connect(self.open_doctor_login)

    def open_admin_login(self):
        self.admin = LoginWindow()
        self.admin.show()
        self.hide()

    def open_doctor_login(self):
        self.doctor = DoctorLoginWindow()
        self.doctor.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
