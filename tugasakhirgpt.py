import time
import random


# ==================== DATA ====================

menu = {
    1: {"nama": "Nasi Goreng", "kategori": "Makanan", "harga": 15000, "stok": 10},
    2: {"nama": "Ayam Geprek", "kategori": "Makanan", "harga": 18000, "stok": 10},
    3: {"nama": "Es Teh", "kategori": "Minuman", "harga": 5000, "stok": 20},
    4: {"nama": "Es Jeruk", "kategori": "Minuman", "harga": 7000, "stok": 15}
}

keranjang = {}
pembayaran = ("Tunai", "Transfer", "E-Wallet")
nomor = {"struk": 0}


# ==================== FUNGSI UMUM ====================

def garis():
    print("=" * 50)


def header(judul):
    garis()
    print(judul.center(50))
    garis()


def format_rupiah(angka):
    teks = str(angka)
    hasil = ""
    hitung = 0
    for i in range(len(teks) - 1, -1, -1):
        hasil = teks[i] + hasil
        hitung = hitung + 1
        if hitung % 3 == 0 and i > 0:
            hasil = "." + hasil
    return "Rp " + hasil


def cek_angka(teks):
    if teks == "":
        return False
    for huruf in teks:
        if huruf not in "0123456789":
            return False
    return True


def input_angka(prompt, min_val=0, max_val=-1):
    while True:
        teks = input(prompt).strip()
        if cek_angka(teks):
            angka = int(teks)
            if angka >= min_val:
                if max_val == -1 or angka <= max_val:
                    return angka
                print("Angka terlalu besar!")
            else:
                print("Angka terlalu kecil!")
        else:
            print("Masukkan angka yang benar!")


def input_teks(prompt):
    while True:
        teks = input(prompt).strip()
        if teks != "":
            return teks
        print("Input tidak boleh kosong!")


def tampilkan_menu(kategori_filter=""):
    if len(menu) == 0:
        print("Menu belum tersedia!")
        return
    for kategori in ("Makanan", "Minuman"):
        if kategori_filter == "" or kategori == kategori_filter:
            print("\n--- " + kategori.upper() + " ---")
            print(f"{'ID':<4}{'Nama':<22}{'Harga':>14}{'Stok':>8}")
            for id, data in menu.items():
                if data["kategori"] == kategori:
                    print(f"{id:<4}{data['nama']:<22}{format_rupiah(data['harga']):>14}{data['stok']:>8}")


# ==================== ADMIN ====================

def login_admin():
    for percobaan in range(3):
        username = input("Username: ")
        password = input("Password: ")
        if username == "admin" and password == "admin123":
            print("Login berhasil!")
            return True
        print("Login gagal! Sisa percobaan: " + str(2 - percobaan))
    return False


def admin_lihat_menu():
    header("DAFTAR MENU")
    tampilkan_menu()


def admin_tambah_menu():
    nama = input_teks("Nama menu: ")
    kategori = input_angka("Kategori (1.Makanan / 2.Minuman): ", 1, 2)
    harga = input_angka("Harga: ", 1)
    stok = input_angka("Stok: ", 0)
    if kategori == 1:
        nama_kategori = "Makanan"
    else:
        nama_kategori = "Minuman"
    id_baru = 1
    for id_lama in menu:
        if id_lama >= id_baru:
            id_baru = id_lama + 1
    menu[id_baru] = {"nama": nama, "kategori": nama_kategori, "harga": harga, "stok": stok}
    print("Menu " + nama + " berhasil ditambahkan dengan ID " + str(id_baru) + "!")


def admin_ubah_menu():
    tampilkan_menu()
    id = input_angka("\nID menu yang diubah: ", 1)
    if id not in menu:
        print("ID menu tidak ditemukan!")
        return
    data = menu[id]
    nama = input("Nama (" + data["nama"] + "): ").strip()
    if nama == "":
        nama = data["nama"]
    kategori = input("Kategori (1.Makanan / 2.Minuman / Enter tetap): ").strip()
    if kategori != "" and kategori != "1" and kategori != "2":
        print("Kategori tidak valid!")
        return
    harga = input("Harga (" + str(data["harga"]) + "): ").strip()
    stok = input("Stok (" + str(data["stok"]) + "): ").strip()
    if harga != "" and cek_angka(harga) == False:
        print("Harga harus berupa angka!")
        return
    if stok != "" and cek_angka(stok) == False:
        print("Stok harus berupa angka!")
        return
    if harga != "" and int(harga) <= 0:
        print("Harga tidak sesuai!")
        return
    if stok != "" and int(stok) < 0:
        print("Stok tidak sesuai!")
        return
    data["nama"] = nama
    if harga != "":
        data["harga"] = int(harga)
    if stok != "":
        data["stok"] = int(stok)
    if kategori == "1":
        data["kategori"] = "Makanan"
    else:
        if kategori == "2":
            data["kategori"] = "Minuman"
    print("Menu berhasil diubah!")


def admin_hapus_menu():
    tampilkan_menu()
    id = input_angka("\nID menu yang dihapus: ", 1)
    if id not in menu:
        print("Menu tidak ditemukan!")
        return
    print(menu[id])
    if input("Yakin hapus? (y/n): ").lower() == "y":
        menu.pop(id)
        keranjang.pop(id, 0)
        print("Menu berhasil dihapus!")


def menu_admin():
    if login_admin() == False:
        return
    aksi = {
        "1": admin_lihat_menu,
        "2": admin_tambah_menu,
        "3": admin_ubah_menu,
        "4": admin_hapus_menu
    }
    jalan = True
    while jalan:
        header("MENU ADMIN")
        print("1. Tampilkan Menu")
        print("2. Tambah Menu")
        print("3. Ubah Menu")
        print("4. Hapus Menu")
        print("5. Logout")
        pilih = input("Pilih: ")
        if pilih in aksi:
            aksi[pilih]()
        else:
            if pilih == "5":
                print("Logout berhasil!")
                jalan = False
            else:
                print("Pilihan tidak valid!")


# ==================== PELANGGAN ====================

def pelanggan_pesan():
    tampilkan_menu()
    id = input_angka("\nID menu yang dipesan (0 batal): ", 0)
    if id == 0:
        return
    if id not in menu:
        print("Menu tidak tersedia!")
        return
    if menu[id]["stok"] <= 0:
        print("Stok habis!")
        return
    jumlah = input_angka("Jumlah pesanan: ", 1)
    total_qty = jumlah
    if id in keranjang:
        total_qty = total_qty + keranjang[id]
    if total_qty > menu[id]["stok"]:
        print("Jumlah pesanan melebihi stok!")
    else:
        keranjang[id] = total_qty
        print("Pesanan berhasil dimasukkan ke keranjang!")


def pelanggan_lihat_keranjang():
    total = 0
    if len(keranjang) == 0:
        print("Keranjang masih kosong!")
        return total
    header("KERANJANG BELANJA")
    print("No  Nama                   Harga       Qty     Subtotal")
    no = 0
    for id, qty in keranjang.items():
        no = no + 1
        subtotal = menu[id]["harga"] * qty
        total = total + subtotal
        print(f"{no:<4}{menu[id]['nama']:<20}{format_rupiah(menu[id]['harga']):>12}{qty:>5}{format_rupiah(subtotal):>14}")
    print("TOTAL: " + format_rupiah(total))
    return total


def pelanggan_hapus_keranjang():
    if len(keranjang) == 0:
        print("Keranjang masih kosong!")
        return
    pelanggan_lihat_keranjang()
    no = input_angka("Nomor item yang dihapus (0 batal): ", 0, len(keranjang))
    if no > 0:
        id = list(keranjang.keys())[no - 1]
        keranjang.pop(id)
        print("Item berhasil dihapus!")


def cetak_struk(total, bayar, kembali, metode):
    nomor["struk"] = random.randint(1000, 9999)
    tanggal = time.strftime("%d-%m-%Y")
    jam = time.strftime("%H:%M:%S")
    header("WARUNG SELERA NUSANTARA")
    print("Jl. Contoh No. 1 | Telp. 08123456789")
    print("No. Struk : #" + str(nomor["struk"]))
    print("Tanggal   : " + tanggal)
    print("Jam       : " + jam)
    print("Kasir     : Admin")
    print("Pembayaran: " + metode)
    garis()
    jumlah_item = 0
    no = 0
    for id, qty in keranjang.items():
        no = no + 1
        data = menu[id]
        subtotal = data["harga"] * qty
        jumlah_item = jumlah_item + qty
        print(str(no) + ". " + data["nama"][:15])
        print("   " + format_rupiah(data["harga"]) + " x " + str(qty) + " = " + format_rupiah(subtotal))
    garis()
    print("Jumlah item : " + str(jumlah_item))
    print("Subtotal    : " + format_rupiah(total))
    print("Diskon      : Rp 0")
    print("TOTAL       : " + format_rupiah(total))
    print("Dibayar     : " + format_rupiah(bayar))
    print("Kembalian   : " + format_rupiah(kembali))
    garis()
    print("Terima kasih telah berbelanja!")
    print("Barang yang sudah dibeli tidak dapat dikembalikan.")
    print("Selamat menikmati!")
    garis()


def pelanggan_checkout():
    if len(keranjang) == 0:
        print("Keranjang masih kosong!")
        return
    total = pelanggan_lihat_keranjang()
    print("\nMetode Pembayaran:")
    no = 0
    for metode in pembayaran:
        no = no + 1
        print(str(no) + ". " + metode)
    pilih = input_angka("Pilih pembayaran: ", 1, len(pembayaran))
    metode = pembayaran[pilih - 1]
    bayar = total
    if metode == "Tunai":
        bayar = input_angka("Uang dibayarkan: Rp ", total)
    kembali = bayar - total
    print("\nTotal: " + format_rupiah(total) + " | Bayar: " + format_rupiah(bayar) + " | Kembali: " + format_rupiah(kembali))
    if input("Konfirmasi pesanan? (y/n): ").lower() == "y":
        for id, qty in keranjang.items():
            menu[id]["stok"] = menu[id]["stok"] - qty
        cetak_struk(total, bayar, kembali, metode)
        keranjang.clear()
    else:
        print("Checkout dibatalkan, keranjang tetap tersimpan!")


def menu_pelanggan():
    aksi = {
        "1": pelanggan_pesan,
        "2": pelanggan_lihat_keranjang,
        "3": pelanggan_hapus_keranjang,
        "4": pelanggan_checkout
    }
    jalan = True
    while jalan:
        header("MENU PELANGGAN")
        print("1. Masukkan Pesanan ke Keranjang")
        print("2. Lihat Keranjang")
        print("3. Hapus dari Keranjang")
        print("4. Checkout")
        print("5. Menu Utama")
        pilih = input("Pilih: ")
        if pilih in aksi:
            aksi[pilih]()
        else:
            if pilih == "5":
                if len(keranjang) > 0:
                    if input("Keranjang akan dikosongkan. Lanjut? (y/n): ").lower() == "y":
                        keranjang.clear()
                        jalan = False
                else:
                    jalan = False
            else:
                print("Pilihan tidak valid!")


# ==================== MENU UTAMA ====================

def menu_utama():
    jalan = True
    while jalan:
        header("FOOD & DRINK ORDERING")
        print("1. Login sebagai Admin")
        print("2. Pesan sebagai Pelanggan")
        print("3. Keluar Program")
        pilih = input("Pilih: ")
        if pilih == "1":
            menu_admin()
        else:
            if pilih == "2":
                menu_pelanggan()
            else:
                if pilih == "3":
                    print("Terima kasih! Program selesai.")
                    jalan = False
                else:
                    print("Pilihan tidak valid!")


menu_utama()
