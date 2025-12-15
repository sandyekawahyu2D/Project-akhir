# riwayat_pemesanan_window.py
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QTableWidgetItem
)
import sys

from riwayat_pemesanan import RiwayatPemesanan


class Ui_RiwayatPemesanan(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(961, 720)

        MainWindow.setStyleSheet("""
QFrame {
    background: #ffffff;
    border-radius: 10px;
}
QPushButton {
    background: #00bfff;
    border-radius: 10px;
    color: white;
    height: 40px;
}
QPushButton:hover {
    background: #87cefa;
}
""")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.label = QtWidgets.QLabel("Riwayat Pemesanan", self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 20, 400, 60))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        self.label.setFont(font)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(40, 110, 880, 460)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID Pemesanan",
            "Username",
            "Nama Tiket",
            "Jumlah",
            "Total Harga",
            "Tanggal"
        ])
        self.tableWidget.setSelectionBehavior(
            QtWidgets.QTableWidget.SelectRows
        )
        self.tableWidget.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers
        )

        self.btn_back = QtWidgets.QPushButton(
            "Kembali", self.centralwidget
        )
        self.btn_back.setGeometry(380, 600, 200, 45)


class RiwayatPemesananWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        self.ui = Ui_RiwayatPemesanan()
        self.ui.setupUi(self)

        self.model = RiwayatPemesanan()

        self.ui.btn_back.clicked.connect(self.back)
        self.load_data()

    def load_data(self):
        self.ui.tableWidget.setRowCount(0)
        data = self.model.select_all()

        for row_idx, row_data in enumerate(data):
            self.ui.tableWidget.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                self.ui.tableWidget.setItem(
                    row_idx,
                    col_idx,
                    QTableWidgetItem(str(value))
                )

    def back(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RiwayatPemesananWindow()
    win.show()
    sys.exit(app.exec_())
