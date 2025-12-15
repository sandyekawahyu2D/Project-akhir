# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from pengguna import Pengguna
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("""
        QWidget { background-color: #f4f6f8; font-family: Arial; }
        QLabel#title { font-size: 28px; font-weight: bold; color: #333; }
        QFrame { background: white; border-radius: 15px; }
        QLineEdit { background-color: #f1f3f4; border-radius: 10px; padding: 12px; font-size: 15px; border: 1px solid #ddd; }
        QPushButton { background-color: #00bfff; color: white; border-radius: 10px; font-size: 16px; font-weight: bold; padding: 12px; }
        QPushButton:hover { background-color: #009acd; }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFixedSize(380, 300)
        self.frame.move(210, 160)

        layout = QtWidgets.QVBoxLayout(self.frame)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.label = QtWidgets.QLabel("Form Login")
        self.label.setObjectName("title")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label)

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Username")
        layout.addWidget(self.lineEdit)

        self.lineEdit_2 = QtWidgets.QLineEdit()
        self.lineEdit_2.setPlaceholderText("Password")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.lineEdit_2)

        self.pushButton = QtWidgets.QPushButton("Login")
        layout.addWidget(self.pushButton)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Login Aplikasi")
        self.ui.pushButton.clicked.connect(self.login)

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        pengguna = Pengguna()
        user = pengguna.login(username, password)

        if user:
            role = user[4]  # level
            QMessageBox.information(self, "Berhasil", f"Login sebagai {role}")

            if role == "admin":
                # Import admin window hanya saat login
                from admin_window import AdminWindow
                self.admin_window = AdminWindow(self)
                self.admin_window.show()
                self.hide()
            else:
                # Import user window
                from user_window import UserWindow
                self.user_window = UserWindow(self, {"id": user[0], "nama": user[3]})
                self.user_window.show()
                self.hide()
        else:
            QMessageBox.warning(self, "Gagal", "Username atau password salah")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
