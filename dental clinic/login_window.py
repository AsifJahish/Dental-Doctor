from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
import bcrypt
from db_connection import get_connection
from admin_dashboard import AdminDashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dental Clinic - Admin Login")
        self.setGeometry(500, 200, 350, 200)

        QLabel("Username:", self).move(30, 40)
        self.username = QLineEdit(self)
        self.username.move(120, 40)

        QLabel("Password:", self).move(30, 80)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.move(120, 80)

        login_btn = QPushButton("Login", self)
        login_btn.move(120, 130)
        login_btn.clicked.connect(self.login)

    def login(self):
        user = self.username.text()
        passwd = self.password.text()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM admin WHERE username=%s", (user,))
        result = cur.fetchone()

        if result and bcrypt.checkpw(passwd.encode(), result[0].encode()):
            QMessageBox.information(self, "Login Successful", "Welcome Admin!")
            self.hide()
            self.dashboard = AdminDashboard()
            self.dashboard.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid Username or Password")

        cur.close()
        conn.close()
