from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox, QMessageBox
from connection import mycursor, mydb
from datetime import datetime

class PemesananWindow(QMainWindow):
    def __init__(self, id_user, parent=None):
        super().__init__(parent)

        self.id_user = id_user
        self.parent_window = parent

        self.setWindowTitle("Pemesanan Tiket")
        self.resize(500, 350)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.cmb_tiket = QComboBox()
        self.spin_jumlah = QSpinBox()
        self.spin_jumlah.setMinimum(1)

        self.btn_pesan = QPushButton("Pesan Tiket")
        self.btn_back = QPushButton("Kembali")

        layout.addWidget(QLabel("Pilih Tiket"))
        layout.addWidget(self.cmb_tiket)
        layout.addWidget(QLabel("Jumlah Tiket"))
        layout.addWidget(self.spin_jumlah)
        layout.addWidget(self.btn_pesan)
        layout.addWidget(self.btn_back)

        self.load_tiket()

        # update max spinbox saat tiket berubah
        self.cmb_tiket.currentIndexChanged.connect(self.on_tiket_changed)

        self.btn_pesan.clicked.connect(self.pesan)
        self.btn_back.clicked.connect(self.back)

    def load_tiket(self):
        self.cmb_tiket.clear()

        sql = "SELECT id_tiket, nama, harga_dasar, stok, tipe FROM tiket WHERE stok > 0"
        mycursor.execute(sql)

        for id_tiket, nama, harga, stok, tipe in mycursor.fetchall():
            self.cmb_tiket.addItem(
                f"{nama} ({tipe}) | Rp{harga:,.0f} | Stok: {stok}",
                (id_tiket, harga, stok)
            )

        self.on_tiket_changed(self.cmb_tiket.currentIndex())

    def on_tiket_changed(self, index):
        if index == -1:
            self.spin_jumlah.setMaximum(1)
            return
        _, _, stok = self.cmb_tiket.itemData(index)
        self.spin_jumlah.setMaximum(stok)
        self.spin_jumlah.setValue(1)

    def pesan(self):
        if self.cmb_tiket.currentIndex() == -1:
            QMessageBox.warning(self, "Error", "Tidak ada tiket tersedia")
            return

        id_tiket, harga, stok = self.cmb_tiket.currentData()
        jumlah = self.spin_jumlah.value()

        if jumlah > stok:
            QMessageBox.warning(self, "Gagal", "Jumlah tiket melebihi stok!")
            return

        total = harga * jumlah

        try:
            # Insert pemesanan
            mycursor.execute(
                "INSERT INTO pemesanan (id_pengguna, id_tiket, tanggal_pesan, jumlah_tiket, total_harga) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.id_user, id_tiket, datetime.now(), jumlah, total)
            )

            # Update stok
            mycursor.execute(
                "UPDATE tiket SET stok = stok - %s WHERE id_tiket = %s",
                (jumlah, id_tiket)
            )

            mydb.commit()
            QMessageBox.information(self, "Sukses", "Tiket berhasil dipesan!")
            self.load_tiket()
        except Exception as e:
            mydb.rollback()
            QMessageBox.critical(self, "Error", str(e))

    def back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()
