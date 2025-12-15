# tiket_vip_window.py
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import sys

from tiket_vip import TiketVIP


class Ui_TiketVIP(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(961, 792)

        MainWindow.setStyleSheet("""
QFrame {
    background: #ffffff;
    border-radius: 10px;
}
QLineEdit {
    background-color: #e8ebea;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
    padding: 10px;
    font-size: 14pt;
}
QPushButton {
    background: #00bfff;
    border-radius: 10px;
    color: white;
    height: 40px;
}
QPushButton:hover {
    background: #87cefa;
    color: #00bfff;
}
""")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.label = QtWidgets.QLabel("Kelola Tiket VIP", self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 20, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        self.label.setFont(font)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(40, 240, 880, 420))

        self.label_NamaTiket = QtWidgets.QLabel("Nama Tiket", self.frame)
        self.label_NamaTiket.move(40, 30)
        self.lineEdit_NamaTiket = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_NamaTiket.setGeometry(200, 20, 640, 45)

        self.label_Harga = QtWidgets.QLabel("Harga Dasar", self.frame)
        self.label_Harga.move(40, 100)
        self.lineEdit_Harga = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Harga.setGeometry(200, 90, 640, 45)
        self.lineEdit_Harga.setValidator(QDoubleValidator(0.0, 99999999.0, 2))

        self.label_Jumlah = QtWidgets.QLabel("Stok", self.frame)
        self.label_Jumlah.move(40, 170)
        self.lineEdit_Jumlah = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Jumlah.setGeometry(200, 160, 640, 45)
        self.lineEdit_Jumlah.setValidator(QIntValidator())

        self.label_Layanan = QtWidgets.QLabel("Biaya Layanan", self.frame)
        self.label_Layanan.move(40, 240)
        self.lineEdit_Layanan = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Layanan.setGeometry(200, 230, 640, 45)
        self.lineEdit_Layanan.setValidator(QDoubleValidator(0.0, 99999999.0, 2))

        self.btn_tambah = QtWidgets.QPushButton("Tambah", self.frame)
        self.btn_tambah.setGeometry(40, 330, 180, 45)

        self.btn_edit = QtWidgets.QPushButton("Edit", self.frame)
        self.btn_edit.setGeometry(250, 330, 180, 45)

        self.btn_hapus = QtWidgets.QPushButton("Hapus", self.frame)
        self.btn_hapus.setGeometry(460, 330, 180, 45)

        self.btn_back = QtWidgets.QPushButton("Kembali", self.frame)
        self.btn_back.setGeometry(670, 330, 180, 45)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(40, 100, 880, 120)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "Nama Tiket", "Harga Dasar",
            "Biaya Layanan", "Stok", "Harga Total"
        ])
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)


class TiketVIPWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        self.ui = Ui_TiketVIP()
        self.ui.setupUi(self)

        self.vip_model = TiketVIP()
        self.selected_id_tiket = None

        self.ui.btn_back.clicked.connect(self.back)
        self.ui.btn_tambah.clicked.connect(self.tambah_data)
        self.ui.btn_edit.clicked.connect(self.edit_data)
        self.ui.btn_hapus.clicked.connect(self.hapus_data)
        self.ui.tableWidget.cellClicked.connect(self.load_selected)

        self.refresh_table()

    # ✅ FIX UTAMA DI SINI
    def back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

    def get_input(self):
        try:
            nama = self.ui.lineEdit_NamaTiket.text().strip()
            harga = float(self.ui.lineEdit_Harga.text() or 0)
            stok = int(self.ui.lineEdit_Jumlah.text() or 0)
            layanan = float(self.ui.lineEdit_Layanan.text() or 0)

            if not nama or harga <= 0:
                raise ValueError

            return nama, harga, stok, layanan
        except:
            QMessageBox.warning(self, "Error", "Input tidak valid")
            return None

    def tambah_data(self):
        data = self.get_input()
        if not data:
            return

        nama, harga, stok, layanan = data
        tiket = TiketVIP(nama=nama, harga_dasar=harga, stok=stok, biaya_layanan=layanan)

        if tiket.insert_data():
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan")
            self.refresh_table()
            self.clear()

    def refresh_table(self):
        self.ui.tableWidget.setRowCount(0)
        data = self.vip_model.select_data_full()

        for row, d in enumerate(data):
            id_, nama, harga, stok, layanan = d
            total = TiketVIP(harga_dasar=harga, biaya_layanan=layanan).hitung_total()

            self.ui.tableWidget.insertRow(row)
            for col, val in enumerate([id_, nama, harga, layanan, stok, total]):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))

    def load_selected(self, row, col):
        self.selected_id_tiket = int(self.ui.tableWidget.item(row, 0).text())
        self.ui.lineEdit_NamaTiket.setText(self.ui.tableWidget.item(row, 1).text())
        self.ui.lineEdit_Harga.setText(self.ui.tableWidget.item(row, 2).text())
        self.ui.lineEdit_Layanan.setText(self.ui.tableWidget.item(row, 3).text())
        self.ui.lineEdit_Jumlah.setText(self.ui.tableWidget.item(row, 4).text())

    def edit_data(self):
        if not self.selected_id_tiket:
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu")
            return

        data = self.get_input()
        if not data:
            return

        nama, harga, stok, layanan = data
        tiket = TiketVIP(
            id_tiket=self.selected_id_tiket,
            nama=nama,
            harga_dasar=harga,
            stok=stok,
            biaya_layanan=layanan
        )

        if tiket.update_data():
            QMessageBox.information(self, "Sukses", "Data diperbarui")
            self.refresh_table()
            self.clear()

    def hapus_data(self):
        if not self.selected_id_tiket:
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu")
            return

        tiket = TiketVIP(id_tiket=self.selected_id_tiket)
        if tiket.delete_data():
            QMessageBox.information(self, "Sukses", "Data dihapus")
            self.refresh_table()
            self.clear()

    def clear(self):
        self.selected_id_tiket = None
        self.ui.lineEdit_NamaTiket.clear()
        self.ui.lineEdit_Harga.clear()
        self.ui.lineEdit_Jumlah.clear()
        self.ui.lineEdit_Layanan.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TiketVIPWindow()
    win.show()
    sys.exit(app.exec_())
