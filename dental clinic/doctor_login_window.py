
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
from PyQt5.QtCore import Qt
import bcrypt
from db_connection import get_connection
from doctor_dashboard import DoctorDashboard

class DoctorLoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # --------- MAKE WINDOW HALF-SCREEN ----------
        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()

        window_width = screen_width // 2
        window_height = screen_height // 2  # or set fixed height like 300

        # Centering the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.setGeometry(x, y, window_width, window_height)
        self.setWindowTitle("Dental Clinic - Doctor Login")

        # -------------------------------------------

        QLabel("Username:", self).move(50, 80)
        self.username = QLineEdit(self)
        self.username.move(160, 80)

        QLabel("Password:", self).move(50, 140)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.move(160, 140)

        login_btn = QPushButton("Login", self)
        login_btn.move(160, 200)
        login_btn.clicked.connect(self.login)

    def login(self):
        user = self.username.text()
        passwd = self.password.text()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM doctors WHERE username=%s", (user,))
        result = cur.fetchone()

        if result and bcrypt.checkpw(passwd.encode(), result[0].encode()):
            QMessageBox.information(self, "Login Successful", "Welcome Doctor!")
            self.hide()
            self.dashboard = DoctorDashboard(user)
            self.dashboard.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid Username or Password")

        cur.close()
        conn.close()
