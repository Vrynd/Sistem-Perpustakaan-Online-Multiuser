import hashlib

class Buku:
    def __init__(self, id_buku, kategori, judul, penulis, tanggal_terbit,  penerbit, jumlah):
        self.id_buku = id_buku
        self.kategori = kategori
        self.judul = judul
        self.penulis = penulis
        self.tanggal_terbit = tanggal_terbit
        self.penerbit = penerbit
        self.jumlah = jumlah

class Anggota:
    def __init__(self, id_anggota, nama_anggota, asal_kota, usia, no_telepon, username, password):
        self.id_anggota = id_anggota
        self.nama_anggota = nama_anggota
        self.asal_kota = asal_kota
        self.usia = usia
        self.no_telepon = no_telepon
        self.username = username
        self.password = password
        self.password_changed = False

    def ganti_password(self, password_baru):
        self.password = hashlib.sha256(password_baru.encode()).hexdigest()
        self.password_changed = True