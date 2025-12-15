from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from connection import mycursor

class RiwayatWindow(QMainWindow):
    def __init__(self, id_user, parent=None):
        super().__init__(parent)
        self.id_user = id_user
        self.parent_window = parent

        self.setWindowTitle("Riwayat Pembelian")
        self.resize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        lbl = QLabel("Riwayat Pembelian Tiket")
        lbl.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(lbl)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.btn_back = QPushButton("Kembali")
        layout.addWidget(self.btn_back)

        self.btn_back.clicked.connect(self.back)

        self.load_data()

    def load_data(self):
        sql = """
        SELECT p.id_pemesanan, t.nama, t.tipe, p.jumlah_tiket, p.total_harga, p.tanggal_pesan
        FROM pemesanan p
        JOIN tiket t ON p.id_tiket = t.id_tiket
        WHERE p.id_pengguna = %s
        ORDER BY p.tanggal_pesan DESC
        """
        mycursor.execute(sql, (self.id_user,))
        rows = mycursor.fetchall()

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nama Tiket", "Tipe", "Jumlah", "Total Harga", "Tanggal Pesan"])
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if j == 4:  # Total harga
                    value = f"Rp{value:,.0f}"
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()

    def back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()
