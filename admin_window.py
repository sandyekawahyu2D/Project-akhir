# admin_dashboard.py
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QVBoxLayout
import sys

from tiket_vip_window import TiketVIPWindow
from tiket_ekonomi_window import TiketEkonomiWindow
from riwayat_pemesanan_window import RiwayatPemesananWindow
from login_window import LoginWindow


# =============================
# UI DASHBOARD ADMIN
# =============================
class Ui_AdminDashboard(object):
    def setupUi(self, main_window):
        main_window.setObjectName("AdminMainWindow")
        main_window.resize(900, 650)

        self.centralwidget = QtWidgets.QWidget(main_window)
        main_window.setCentralWidget(self.centralwidget)

        # ===== JUDUL =====
        self.label_title = QtWidgets.QLabel(
            "DASHBOARD ADMINISTRATOR", self.centralwidget
        )
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setGeometry(QtCore.QRect(0, 40, 900, 60))
        self.label_title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
        """)

        # ===== FRAME MENU =====
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(250, 150, 400, 450))
        self.frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 14px;
            }
        """)

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # ===== BUTTON =====
        self.btn_vip = QtWidgets.QPushButton("Kelola Tiket VIP")
        self.btn_eko = QtWidgets.QPushButton("Kelola Tiket Ekonomi")
        self.btn_riwayat = QtWidgets.QPushButton("Riwayat Pemesanan")
        self.btn_logout = QtWidgets.QPushButton("Logout")

        for btn in [
            self.btn_vip,
            self.btn_eko,
            self.btn_riwayat,
            self.btn_logout
        ]:
            btn.setFixedHeight(45)
            btn.setStyleSheet("""
                QPushButton {
                    background: #00bfff;
                    color: white;
                    font-size: 14px;
                    border-radius: 12px;
                }
                QPushButton:hover {
                    background: #87cefa;
                }
            """)

        layout.addWidget(self.btn_vip)
        layout.addWidget(self.btn_eko)
        layout.addWidget(self.btn_riwayat)
        layout.addStretch()
        layout.addWidget(self.btn_logout)


# =============================
# LOGIC DASHBOARD ADMIN
# =============================
class AdminWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent

        self.ui = Ui_AdminDashboard()
        self.ui.setupUi(self)
        self.setWindowTitle("Admin Dashboard")

        # ===== SIMPAN INSTANCE WINDOW =====
        self.vip_window = None
        self.eko_window = None
        self.riwayat_window = None

        # ===== CONNECT BUTTON =====
        self.ui.btn_vip.clicked.connect(self.kelola_vip)
        self.ui.btn_eko.clicked.connect(self.kelola_ekonomi)
        self.ui.btn_riwayat.clicked.connect(self.riwayat)
        self.ui.btn_logout.clicked.connect(self.logout)

    # =============================
    # NAVIGASI WINDOW
    # =============================
    def kelola_vip(self):
        if self.vip_window is None:
            self.vip_window = TiketVIPWindow(self)

        self.vip_window.show()
        self.hide()

    def kelola_ekonomi(self):
        if self.eko_window is None:
            self.eko_window = TiketEkonomiWindow(self)

        self.eko_window.show()
        self.hide()

    def riwayat(self):
        if self.riwayat_window is None:
            self.riwayat_window = RiwayatPemesananWindow(self)

        self.riwayat_window.show()
        self.hide()

    # =============================
    # LOGOUT
    # =============================
    def logout(self):
        confirm = QMessageBox.question(
            self,
            "Konfirmasi Logout",
            "Yakin ingin logout?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.close()

            if self.parent_window and isinstance(self.parent_window, LoginWindow):
                self.parent_window.show()
            else:
                self.login_window = LoginWindow()
                self.login_window.show()


# =============================
# TESTING
# =============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec_())
