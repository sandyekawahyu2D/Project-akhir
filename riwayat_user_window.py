from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from pemesanan_window import PemesananWindow
from riwayat_window import RiwayatWindow  # import riwayat

class UserWindow(QMainWindow):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent_window = parent
        self.user = user  # {"id": id_user, "nama": nama_user}

        self.setWindowTitle("Dashboard User")
        self.resize(500, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        lbl = QLabel(f"Selamat Datang, {self.user['nama']}")
        lbl.setStyleSheet("font-size:20px; font-weight:bold;")
        lbl.setAlignment(Qt.AlignCenter)

        btn_pesan = QPushButton("Pesan Tiket")
        btn_riwayat = QPushButton("Riwayat Pembelian")
        btn_logout = QPushButton("Logout")

        btn_pesan.setFixedHeight(40)
        btn_riwayat.setFixedHeight(40)
        btn_logout.setFixedHeight(40)

        layout.addWidget(lbl)
        layout.addWidget(btn_pesan)
        layout.addWidget(btn_riwayat)
        layout.addWidget(btn_logout)

        central.setLayout(layout)

        btn_pesan.clicked.connect(self.open_pemesanan)
        btn_riwayat.clicked.connect(self.open_riwayat)
        btn_logout.clicked.connect(self.logout)

    def open_pemesanan(self):
        self.pemesanan_window = PemesananWindow(self.user['id'], self)
        self.pemesanan_window.show()
        self.hide()

    def open_riwayat(self):
        self.riwayat_window = RiwayatWindow(self.user['id'], self)
        self.riwayat_window.show()
        self.hide()

    def logout(self):
        self.parent_window.show()
        self.close()
