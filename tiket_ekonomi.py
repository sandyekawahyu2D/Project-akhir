from tiket import Tiket
from connection import mycursor

class TiketEkonomi(Tiket):

    def __init__(self):
        super().__init__()

    def hitung_total(self, id_tiket, jumlah):
        sql = "SELECT harga_dasar FROM tiket WHERE id_tiket = %s"
        mycursor.execute(sql, (id_tiket,))
        harga_dasar = mycursor.fetchone()[0]

        return harga_dasar * jumlah
