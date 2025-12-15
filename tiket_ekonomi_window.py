# tiket_ekonomi_window.py
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import sys

from tiket_ekonomi import TiketEkonomi


class Ui_TiketEkonomi(object):
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

        self.label = QtWidgets.QLabel("Kelola Tiket EKONOMI", self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 20, 450, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        self.label.setFont(font)

        # ================= FRAME FORM =================
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

        self.label_Stok = QtWidgets.QLabel("Stok", self.frame)
        self.label_Stok.move(40, 170)
        self.lineEdit_Stok = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Stok.setGeometry(200, 160, 640, 45)
        self.lineEdit_Stok.setValidator(QIntValidator())

        self.label_Zona = QtWidgets.QLabel("Zona", self.frame)
        self.label_Zona.move(40, 240)
        self.lineEdit_Zona = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_Zona.setGeometry(200, 230, 640, 45)

        self.btn_tambah = QtWidgets.QPushButton("Tambah", self.frame)
        self.btn_tambah.setGeometry(40, 330, 180, 45)

        self.btn_edit = QtWidgets.QPushButton("Edit", self.frame)
        self.btn_edit.setGeometry(250, 330, 180, 45)

        self.btn_hapus = QtWidgets.QPushButton("Hapus", self.frame)
        self.btn_hapus.setGeometry(460, 330, 180, 45)

        self.btn_back = QtWidgets.QPushButton("Kembali", self.frame)
        self.btn_back.setGeometry(670, 330, 180, 45)

        # ================= TABLE =================
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(40, 100, 880, 120)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "Nama Tiket", "Harga Dasar", "Stok", "Zona"
        ])
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)


class TiketEkonomiWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        self.ui = Ui_TiketEkonomi()
        self.ui.setupUi(self)

        self.ekonomi_model = TiketEkonomi()
        self.selected_id_tiket = None

        self.ui.btn_back.clicked.connect(self.back)
        self.ui.btn_tambah.clicked.connect(self.tambah_data)
        self.ui.btn_edit.clicked.connect(self.edit_data)
        self.ui.btn_hapus.clicked.connect(self.hapus_data)
        self.ui.tableWidget.cellClicked.connect(self.load_selected)

        self.refresh_table()

    # ================= NAVIGASI =================
    def back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

    # ================= INPUT =================
    def get_input(self):
        try:
            nama = self.ui.lineEdit_NamaTiket.text().strip()
            harga = float(self.ui.lineEdit_Harga.text() or 0)
            stok = int(self.ui.lineEdit_Stok.text() or 0)
            zona = self.ui.lineEdit_Zona.text().strip()

            if not nama or harga <= 0 or not zona:
                raise ValueError

            return nama, harga, stok, zona
        except:
            QMessageBox.warning(self, "Error", "Input tidak valid")
            return None

    # ================= CRUD =================
    def tambah_data(self):
        data = self.get_input()
        if not data:
            return

        nama, harga, stok, zona = data
        tiket = TiketEkonomi(nama=nama, harga_dasar=harga, stok=stok, zona=zona)

        if tiket.insert_data():
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan")
            self.refresh_table()
            self.clear()

    def refresh_table(self):
        self.ui.tableWidget.setRowCount(0)
        data = self.ekonomi_model.select_data_full()

        for row, d in enumerate(data):
            self.ui.tableWidget.insertRow(row)
            for col, val in enumerate(d):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(val)))

    def load_selected(self, row, col):
        self.selected_id_tiket = int(self.ui.tableWidget.item(row, 0).text())
        self.ui.lineEdit_NamaTiket.setText(self.ui.tableWidget.item(row, 1).text())
        self.ui.lineEdit_Harga.setText(self.ui.tableWidget.item(row, 2).text())
        self.ui.lineEdit_Stok.setText(self.ui.tableWidget.item(row, 3).text())
        self.ui.lineEdit_Zona.setText(self.ui.tableWidget.item(row, 4).text())

    def edit_data(self):
        if not self.selected_id_tiket:
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu")
            return

        data = self.get_input()
        if not data:
            return

        nama, harga, stok, zona = data
        tiket = TiketEkonomi(
            id_tiket=self.selected_id_tiket,
            nama=nama,
            harga_dasar=harga,
            stok=stok,
            zona=zona
        )

        if tiket.update_data():
            QMessageBox.information(self, "Sukses", "Data diperbarui")
            self.refresh_table()
            self.clear()

    def hapus_data(self):
        if not self.selected_id_tiket:
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu")
            return

        tiket = TiketEkonomi(id_tiket=self.selected_id_tiket)
        if tiket.delete_data():
            QMessageBox.information(self, "Sukses", "Data dihapus")
            self.refresh_table()
            self.clear()

    def clear(self):
        self.selected_id_tiket = None
        self.ui.lineEdit_NamaTiket.clear()
        self.ui.lineEdit_Harga.clear()
        self.ui.lineEdit_Stok.clear()
        self.ui.lineEdit_Zona.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TiketEkonomiWindow()
    win.show()
    sys.exit(app.exec_())
