# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import sys
from login_window import LoginWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 650)
        MainWindow.setStyleSheet("""
        QWidget {
            background-color: #f4f6f8;
            font-family: Arial;
        }
        QLabel#title {
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }
        QFrame {
            background: white;
            border-radius: 20px;
        }
        QPushButton {
            background-color: #00bfff;
            color: white;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            padding: 14px;
        }
        QPushButton:hover {
            background-color: #009acd;
        }
        QPushButton#logout {
            background-color: #ff4d4d;
        }
        QPushButton#logout:hover {
            background-color: #e60000;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.label = QtWidgets.QLabel("DASHBOARD ADMIN", self.centralwidget)
        self.label.setObjectName("title")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setGeometry(QtCore.QRect(0, 40, 900, 60))

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(200, 130, 500, 450))

        layout = QtWidgets.QVBoxLayout(self.frame)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        self.btn_vip = QtWidgets.QPushButton("Kelola Tiket VIP")
        self.btn_eko = QtWidgets.QPushButton("Kelola Tiket Ekonomi")
        self.btn_riwayat = QtWidgets.QPushButton("Riwayat Pembelian")
        self.btn_user = QtWidgets.QPushButton("Kelola User")

        self.btn_logout = QtWidgets.QPushButton("Logout")
        self.btn_logout.setObjectName("logout")

        layout.addWidget(self.btn_vip)
        layout.addWidget(self.btn_eko)
        layout.addWidget(self.btn_riwayat)
        layout.addWidget(self.btn_user)
        layout.addStretch()
        layout.addWidget(self.btn_logout)


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_vip.clicked.connect(self.kelola_vip)
        self.ui.btn_eko.clicked.connect(self.kelola_ekonomi)
        self.ui.btn_riwayat.clicked.connect(self.riwayat)
        self.ui.btn_user.clicked.connect(self.kelola_user)
        self.ui.btn_logout.clicked.connect(self.logout)

    def kelola_vip(self):
        QMessageBox.information(self, "Info", "Buka Kelola Tiket VIP")

    def kelola_ekonomi(self):
        QMessageBox.information(self, "Info", "Buka Kelola Tiket Ekonomi")

    def riwayat(self):
        QMessageBox.information(self, "Info", "Buka Riwayat Pembelian")

    def kelola_user(self):
        QMessageBox.information(self, "Info", "Buka Kelola User")

    def logout(self):
        confirm = QMessageBox.question(
            self, "Logout", "Yakin ingin logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.close()
            self.login = LoginWindow()
            self.login.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec_())
