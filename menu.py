import time
from perpustakaan import Perpustakaan

def hitung_mundur(detik):
    while detik:
        menit, detik_sisa = divmod(detik, 60)
        timer = '{:02d}:{:02d}'.format(menit, detik_sisa)
        print(f"Silakan tunggu selama {detik_sisa} detik...", end="\r")
        time.sleep(1)
        detik -= 1
    print("Waktu tunggu selesai. Silakan coba login kembali.")

def main():
    perpus = Perpustakaan()
    percobaan_login = 3
    while percobaan_login > 0:
        print("\n=== Sistem Login Perpustakaan ===")
        username = input("Username: ")
        password = input("Password: ")
        user_type = perpus.login(username, password)

        if user_type == "admin":
            print(f"Login Berhasil. Selamat datang, {username}!")
            percobaan_login = 3
            while True:
                print("\n=== Dashboard Admin ===")
                print("1. Tambah Buku")
                print("2. Lihat Daftar Buku")
                print("3. Tambah Anggota")
                print("4. Lihat Anggota")
                print("0. Logout")
                pilihan = input("Pilih menu: ")
                if pilihan == '1':
                    id_buku = input("ID Buku: ")
                    kategori = input("Kategori Buku : ")
                    judul = input("Judul Buku: ")
                    penulis = input("Penulis Buku: ")
                    tanggal_terbit = input("Tanggal Terbit (DD-MM-YYYY): ")
                    penerbit = input("Penerbit: ")
                    jumlah = int(input("Jumlah Buku: "))
                    perpus.tambah_buku(id_buku, kategori, judul, penulis, tanggal_terbit, penerbit, jumlah)

                elif pilihan == '2':
                    perpus.tampilkan_buku()

                elif pilihan == '3':
                    nama_lengkap = input("Nama sesuai KTP: ")
                    asal_kota = input("Kota Asal: ")
                    usia = input("Usia: ")
                    no_telepon = input("Masukkan No. Telepon yang bisa dihubungi : ")
                    if len(no_telepon) >= 12 and len(no_telepon) <= 15:
                        perpus.tambah_anggota(nama_lengkap, asal_kota, usia, no_telepon)
                    else:
                        print("Nomor telepon tidak valid. Coba lagi!")
                elif pilihan == '4':
                    perpus.tampilkan_anggota()

                elif pilihan == '0':
                    print("Anda telah logout.")
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")

        elif user_type and user_type[0] == "user":
            id_anggota = user_type[1]
            anggota = perpus.daftar_anggota[id_anggota]
            print(f"Login Berhasil. Selamat datang, Anggota {username}!")

            if not anggota.password_changed:
                while True:
                    response = input("\nApakah Anda ingin mengganti password Anda? (y/t) : ").strip().lower()
                    if response == 'y':
                        while True:
                            pattern_info = ("Password harus memenuhi kriteria berikut:\n"
                                            "1. Password minimal 8 karakter.\n"
                                            "2. Mengandung setidaknya satu simbol.\n"
                                            "3. Mengandung setidaknya satu huruf besar.\n"
                                            "4. Mengandung setidaknya satu angka.\n")
                            print(pattern_info)
                            password_baru = input("Masukkan password baru: ")
                            if perpus.valid_password(password_baru):
                                perpus.ganti_password_anggota(id_anggota, password_baru)
                                break
                            else:
                                print("Password tidak sesuai dengan karakter yang ditentukan. Silakan coba lagi.")
                        break
                    elif response == 't':
                        break
                    else:
                        print("Pilihan tidak valid. Silakan coba lagi.")

            while True:
                print("\n=== Dashboard Anggota ===")
                print("1. Lihat Daftar Buku")
                print("2. Pinjam Buku")
                print("3. Kembalikan Buku")
                print("0. Logout")
                pilihan = input("Pilih menu: ")
                if pilihan == '1':
                    perpus.tampilkan_buku()

                elif pilihan == '2':
                    kategori = input("Cari buku [berdasarkan jenis buku]: ")
                    hasil_pencarian = perpus.cari_buku(kategori)
                    if hasil_pencarian:
                        perpus.tampilkan_pinjam_buku(hasil_pencarian)
                        id_buku = input("ID buku yang ingin dipinjam: ")
                        durasi = int(input("Durasi peminjaman (dalam hari): "))
                        perpus.pinjam_buku(id_buku, id_anggota, durasi)
                    else:
                        print("Tidak ada buku yang ditemukan untuk kategori tersebut.")

                elif pilihan == '3':
                    id_buku = input("ID Buku yang ingin dikembalikan: ")
                    perpus.kembalikan_buku(id_buku, id_anggota)

                elif pilihan == '0':
                    print("Anda telah logout.")
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
        else:
            percobaan_login -= 1
            if percobaan_login > 0:
                print(f"Login Gagal! Username atau password salah. Anda memiliki {percobaan_login} percobaan lagi.")
            else:
                print("Login Gagal! Anda telah melebihi batas percobaan login")
                coba_lagi = input("Apakah anda ingin menunggu selama 30 detik atau keluar dari sistem (y/t) : ").strip().lower()
                if coba_lagi == 'y':
                    hitung_mundur(30)
                    percobaan_login = 3
                elif coba_lagi == 't':
                    print("Anda telah keluar dari sistem.")
                    return
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
if __name__ == "__main__":
    main()