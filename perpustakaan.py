import re
import random
import hashlib
from datetime import datetime, timedelta
from dataset import Buku, Anggota
from tabulate import tabulate

class Perpustakaan:
    def __init__(self):
        self.daftar_buku = {}
        self.daftar_anggota = {}
        self.transaksi = []
        self.admins = {"admin": "Admin123#"}
        self.nomor_registrasi = "16"
        self.tahun_buka = "24"
        self.urutan_anggota = 1

    def generate_id_anggota(self):
        id_anggota = f"{self.tahun_buka}{self.nomor_registrasi}{self.urutan_anggota:02d}"
        self.urutan_anggota += 1
        return id_anggota

    def generate_username(self, nama_lengkap):
        nama_parts = nama_lengkap.split()
        if len(nama_parts) >= 2:
            return nama_parts[0].lower() + nama_parts[1].lower()
        return nama_parts[0].lower()

    def generate_password(self):
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
        return ''.join(random.choices(characters, k=12))

    def tambah_buku(self, id_buku, kategori, judul, penulis, tanggal_terbit, penerbit, jumlah):
        if id_buku not in self.daftar_buku:
            self.daftar_buku[id_buku] = Buku(id_buku,  kategori, judul, penulis, tanggal_terbit, penerbit, jumlah)
            print(f"Buku dengan '{judul}' telah ditambahkan.")
        else:
            print(f"Buku dengan ID {id_buku} sudah ada.")

    def tampilkan_buku(self):
        data = []
        headers = ["ID","Jenis Buku", "Judul", "Penulis", "Tanggal Terbit", "Penerbit" , "Jumlah"]
        for buku in self.daftar_buku.values():
            data.append([buku.id_buku, buku.kategori, buku.judul, buku.penulis, buku.tanggal_terbit, buku.penerbit, buku.jumlah])
        print(tabulate(data, headers, tablefmt="grid"))

    def tambah_anggota(self, nama_anggota, asal_kota, usia, no_telepon):
        id_anggota = self.generate_id_anggota()
        username = self.generate_username(nama_anggota)
        password = self.generate_password()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.daftar_anggota[id_anggota] = Anggota(id_anggota, nama_anggota, asal_kota, usia,no_telepon, username, password_hash)
        print(f"{nama_anggota} Telah ditambahkan sebagai anggota baru. Silahkan login dengan Username: {username} dan Password: {password}")

    def tampilkan_anggota(self):
        data = []
        headers = ["ID", "Nama Anggota", "Asal Kota", "Usia", "Username", "Password", "No.Telepon"]
        for anggota in self.daftar_anggota.values():
            data.append([anggota.id_anggota, anggota.nama_anggota, anggota.asal_kota, anggota.usia, anggota.no_telepon, anggota.username, anggota.password])
        print(tabulate(data, headers, tablefmt="grid"))

    def pinjam_buku(self, id_buku, id_anggota, durasi):
        if id_buku in self.daftar_buku and id_anggota in self.daftar_anggota:
            buku = self.daftar_buku[id_buku]
            if buku.jumlah > 0:
                buku.jumlah -= 1
                tanggal_peminjaman = datetime.now()
                tanggal_pengembalian = tanggal_peminjaman + timedelta(days=durasi)
                self.transaksi.append((id_anggota, id_buku, tanggal_peminjaman, tanggal_pengembalian, durasi))
                print(f"Buku dengan ID {id_buku} telah berhasil dipinjam.")
                print(f"Durasi peminjaman: {durasi} hari")
                print(f"Tanggal peminjaman: {tanggal_peminjaman.strftime('%d-%m-%Y')}")
                print(f"Tanggal pengembalian: {tanggal_pengembalian.strftime('%d-%m-%Y')}")
            else:
                print(f"Buku dengan ID {id_buku} sedang tidak tersedia.")
        else:
            print(f"ID buku {id_buku} atau ID anggota {id_anggota} tidak ditemukan.")

    def tampilkan_pinjam_buku(self, hasil_pencarian):
        data_pinjam = []
        headers = ["ID", "Kategori", "Judul", "Penulis", "Tanggal Terbit", "Penerbit", "Jumlah"]
        for buku in hasil_pencarian:
            data_pinjam.append([buku.id_buku, buku.kategori, buku.judul, buku.penulis, buku.tanggal_terbit, buku.penerbit, buku.jumlah])
        print(tabulate(data_pinjam, headers, tablefmt="grid"))

    def cari_buku(self, kategori):
        hasil_pencarian = []
        for buku in self.daftar_buku.values():
            if buku.kategori.lower() == kategori.lower():
                hasil_pencarian.append(buku)
        return hasil_pencarian

    def kembalikan_buku(self, id_buku, id_anggota):
        if id_buku in self.daftar_buku and id_anggota in self.daftar_anggota:
            buku = self.daftar_buku[id_buku]
            buku.jumlah += 1
            self.transaksi.append((id_anggota, id_buku, "kembali"))
            print(f"Anggota dengan ID {id_anggota} telah mengembalikan buku '{buku.judul}'.")
        else:
            print("ID buku atau anggota tidak ditemukan.")

    def login(self, username, password):
        if username in self.admins and self.admins[username] == password:
            return "admin"
        for anggota in self.daftar_anggota.values():
            if anggota.username == username and anggota.password == hashlib.sha256(password.encode()).hexdigest():
                return "user", anggota.id_anggota
        return None

    def ganti_password_anggota(self, id_anggota, password_baru):
        self.daftar_anggota[id_anggota].ganti_password(password_baru)
        print("Password berhasil diubah.")

    def valid_password(self, password):
        pattern = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}')
        return pattern.match(password)