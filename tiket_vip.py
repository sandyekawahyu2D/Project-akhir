from tiket import Tiket
from connection import mycursor

class TiketVIP(Tiket):

    def __init__(self):
        super().__init__()

    # method hitung_total()
    def hitung_total(self, id_tiket, jumlah):
        sql = """
        SELECT t.harga_dasar, v.biaya_layanan
        FROM tiket t
        JOIN tiket_vip v ON t.id_tiket = v.id_tiket
        WHERE t.id_tiket = %s
        """
        mycursor.execute(sql, (id_tiket,))
        harga_dasar, biaya_layanan = mycursor.fetchone()

        return (harga_dasar + biaya_layanan) * jumlah
