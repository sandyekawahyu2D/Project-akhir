# tiket_vip.py

from connection import mycursor, mydb
from tiket import Tiket 

class TiketVIP(Tiket):
    """Kelas TiketVIP mewarisi dari Tiket dan menangani tabel 'tiket_vip'."""
    def __init__(self, id_tiket=None, nama=None, harga_dasar=None, stok=None, biaya_layanan=None):
        super().__init__(id_tiket, nama, harga_dasar, stok)
        self.biaya_layanan = biaya_layanan

    def hitung_total(self) -> float:
        """Menghitung total harga (Harga Dasar + Biaya Layanan)."""
        if self.harga_dasar is None or self.biaya_layanan is None:
             return 0.0
        return self.harga_dasar + self.biaya_layanan
    
    def select_data_full(self):
        """Mengambil data lengkap Tiket VIP dari tabel 'tiket' dan 'tiket_vip'."""
        sql = """
        SELECT t.id_tiket, t.nama, t.harga_dasar, t.stok, tv.biaya_layanan
        FROM tiket t
        JOIN tiket_vip tv ON t.id_tiket = tv.id_tiket
        """
        mycursor.execute(sql)
        return mycursor.fetchall()

    def insert_data(self):
        """Menyimpan data baru ke tabel 'tiket' dan 'tiket_vip'."""
        try:
            sql_tiket = "INSERT INTO tiket (nama, harga_dasar, stok) VALUES (%s, %s, %s)"
            mycursor.execute(sql_tiket, (self.nama, self.harga_dasar, self.stok))
            self.id_tiket = mycursor.lastrowid
            
            sql_vip = "INSERT INTO tiket_vip (id_tiket, biaya_layanan) VALUES (%s, %s)"
            mycursor.execute(sql_vip, (self.id_tiket, self.biaya_layanan))
            
            mydb.commit()
            return True
        except Exception as e:
            mydb.rollback()
            print(f"Error saat insert data VIP: {e}")
            return False

    def update_data(self):
        """Memperbarui data di tabel 'tiket' dan 'tiket_vip'."""
        if self.id_tiket is None: return False
            
        try:
            sql_tiket = "UPDATE tiket SET nama = %s, harga_dasar = %s, stok = %s WHERE id_tiket = %s"
            mycursor.execute(sql_tiket, (self.nama, self.harga_dasar, self.stok, self.id_tiket))
            
            sql_vip = "UPDATE tiket_vip SET biaya_layanan = %s WHERE id_tiket = %s"
            mycursor.execute(sql_vip, (self.biaya_layanan, self.id_tiket))
            
            mydb.commit()
            return True
        except Exception as e:
            mydb.rollback()
            print(f"Error saat update data VIP: {e}")
            return False

    def delete_data(self):
        """Menghapus data dari tabel 'tiket' (menghapus juga dari tiket_vip jika CASCADE)."""
        if self.id_tiket is None: return False
            
        try:
            sql = "DELETE FROM tiket WHERE id_tiket = %s"
            mycursor.execute(sql, (self.id_tiket,))
            
            mydb.commit()
            return True
        except Exception as e:
            mydb.rollback()
            print(f"Error saat delete data VIP: {e}")
            return False