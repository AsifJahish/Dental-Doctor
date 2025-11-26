

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,
    QApplication, QVBoxLayout, QHBoxLayout, QFrame
)
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
        window_height = screen_height // 2

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.setGeometry(x, y, window_width, window_height)
        self.setWindowTitle("Dental Clinic - Doctor Login")
        self.setStyleSheet("background-color: #f0f2f5;")

        # ========= MAIN LAYOUT =========
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # -------- CARD FRAME (WHITE BOX) --------
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 30px;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
            QLineEdit {
                font-size: 25px;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #bfc3c7;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #2b7cff;
                color: white;
                font-size: 25px;
                padding: 10px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5b9aff;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setSpacing(20)

        # ---------- Username ----------
        username_label = QLabel("Username:")
        self.username = QLineEdit()
        card_layout.addWidget(username_label)
        card_layout.addWidget(self.username)

        # ---------- Password ----------
        password_label = QLabel("Password:")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.password)

        # ---------- Login Button ----------
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        card_layout.addWidget(login_btn)

        card.setLayout(card_layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

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
