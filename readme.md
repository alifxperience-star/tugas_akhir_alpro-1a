# Notulensi — Alur Kerja `tugasakhirgpt.py`

| Keterangan  | Isi                                                                |
| ----------- | ------------------------------------------------------------------ |
| **Program** | `tugasakhirgpt.py`                                                 |
| **Jenis**   | Aplikasi pemesanan makanan dan minuman berbasis console            |
| **Bahasa**  | Python                                                             |
| **Tanggal** | 26 November 2026                                                   |
| **Topik**   | Proses kerja program mulai dari menu utama hingga pencetakan struk |

## Ringkasan

Program ini menyediakan dua peran: **admin**, yang mengelola data menu, dan **pelanggan**, yang memesan barang, mengelola keranjang, serta melakukan pembayaran. Seluruh interaksi terjadi melalui teks di console. Perubahan data bersifat sementara dan hanya berlaku selama program berjalan.

## Daftar Isi

1. [Konsep dan Library](#1-konsep-dan-library)
2. [Struktur Data](#2-struktur-data)
3. [Daftar Fungsi](#3-daftar-fungsi)
4. [Alur Umum Program](#4-alur-umum-program)
5. [Alur Admin](#5-alur-admin)
6. [Alur Pelanggan](#6-alur-pelanggan)
7. [Alur Checkout dan Struk](#7-alur-checkout-dan-struk)
8. [Aturan Validasi Input](#8-aturan-validasi-input)
9. [Cara Menjalankan](#9-cara-menjalankan)
10. [Catatan Tambahan](#10-catatan-tambahan)

---

## 1. Konsep dan Library

### 1.1 Konsep yang digunakan

Program sengaja dibuat sederhana dengan batasan konsep berikut.

| Konsep        | Penggunaan dalam program                                                                           |
| ------------- | -------------------------------------------------------------------------------------------------- |
| `if` / `else` | Percabangan keputusan, termasuk pengganti `elif`                                                   |
| `function`    | `def` dan `return`, serta fungsi bawaan seperti `input`, `print`, `str`, `int`, `len`, dan `range` |
| `dictionary`  | Penyimpanan data menu, keranjang, nomor struk, dan pemetaan pilihan menu                           |
| `list`        | Daftar kunci keranjang saat memilih item untuk dihapus                                             |
| `tuple`       | Daftar metode pembayaran dan daftar kategori menu                                                  |
| `operator`    | `+`, `-`, `*`, `%`, `==`, `!=`, `>=`, `<=`, `in`, `and`, `or`                                      |
| `while`       | Perulangan menu hingga pengguna memilih keluar                                                     |
| `for`         | Perulangan tampilan menu, item keranjang, dan percobaan login                                      |

Konsep yang **tidak** digunakan: `try/except`, `elif`, `break`, `continue`, `global`, `del`, `class`, dan komprehensif list.

### 1.2 Library yang digunakan

| Library  | Kegunaan                                                         |
| -------- | ---------------------------------------------------------------- |
| `time`   | Menampilkan tanggal (`%d-%m-%Y`) dan jam (`%H:%M:%S`) pada struk |
| `random` | Membuat nomor struk acak 4 digit melalui `randint(1000, 9999)`   |

Keduanya merupakan library bawaan Python, sehingga tidak memerlukan instalasi tambahan.

---

## 2. Struktur Data

```python
menu = {
    1: {"nama": "Nasi Goreng", "kategori": "Makanan", "harga": 15000, "stok": 10},
    2: {"nama": "Ayam Geprek", "kategori": "Makanan", "harga": 18000, "stok": 10},
    3: {"nama": "Es Teh",      "kategori": "Minuman", "harga": 5000,  "stok": 20},
    4: {"nama": "Es Jeruk",    "kategori": "Minuman", "harga": 7000,  "stok": 15}
}

keranjang  = {}                        # {id_menu: jumlah_pesanan}
pembayaran = ("Tunai", "Transfer", "E-Wallet")
nomor      = {"struk": 0}              # diisi nomor acak saat struk dicetak
```

| Variabel     | Jenis      | Fungsi                                                 |
| ------------ | ---------- | ------------------------------------------------------ |
| `menu`       | Dictionary | Menyimpan data barang: nama, kategori, harga, dan stok |
| `keranjang`  | Dictionary | Menyimpan barang pesanan yang belum di-checkout        |
| `pembayaran` | Tuple      | Menyimpan tiga pilihan metode pembayaran               |
| `nomor`      | Dictionary | Menyimpan nomor struk yang dihasilkan secara acak      |

---

## 3. Daftar Fungsi

| Fungsi                        | Tugas singkat                                                       |
| ----------------------------- | ------------------------------------------------------------------- |
| `garis()`                     | Mencetak garis pembatas sepanjang 50 karakter                       |
| `header(judul)`               | Mencetak judul di antara dua garis pembatas                         |
| `format_rupiah(angka)`        | Mengubah angka menjadi format `Rp 15.000`                           |
| `cek_angka(teks)`             | Memeriksa apakah teks hanya berisi angka                            |
| `input_angka(...)`            | Meminta angka yang valid sesuai batas minimum dan maksimum          |
| `input_teks(prompt)`          | Meminta teks dan menolak input kosong                               |
| `tampilkan_menu(...)`         | Menampilkan menu, dapat difilter berdasarkan kategori               |
| `login_admin()`               | Memeriksa kredensial admin, maksimal tiga percobaan                 |
| `admin_lihat_menu()`          | Menampilkan seluruh menu                                            |
| `admin_tambah_menu()`         | Menambah menu baru dengan ID otomatis                               |
| `admin_ubah_menu()`           | Mengubah nama, kategori, harga, dan stok menu                       |
| `admin_hapus_menu()`          | Menghapus menu beserta datanya dari keranjang                       |
| `menu_admin()`                | Mengatur perulangan menu admin                                      |
| `pelanggan_pesan()`           | Memasukkan pesanan ke keranjang setelah memeriksa stok              |
| `pelanggan_lihat_keranjang()` | Menampilkan keranjang dan mengembalikan nilai total                 |
| `pelanggan_hapus_keranjang()` | Menghapus item berdasarkan nomor urut                               |
| `cetak_struk(...)`            | Mencetak struk berisi tanggal, jam, nomor acak, dan rincian belanja |
| `pelanggan_checkout()`        | Memproses pembayaran, mengurangi stok, dan mencetak struk           |
| `menu_pelanggan()`            | Mengatur perulangan menu pelanggan                                  |
| `menu_utama()`                | Mengatur perulangan menu utama sebagai titik masuk program          |

---

## 4. Alur Umum Program

```text
MULAI
  |
  v
menu_utama()  -- while jalan:
  |
  +-- pilih "1" --> menu_admin()
  |
  +-- pilih "2" --> menu_pelanggan()
  |
  +-- pilih "3" --> jalan = False --> SELESAI
  |
  `-- pilihan lain --> "Pilihan tidak valid!" --> ulang
```

Perulangan menggunakan variabel `jalan` yang bernilai `True` selama menu aktif. Variabel diubah menjadi `False` saat pengguna memilih keluar. Pola ini menggantikan `break` dan dipakai kembali di `menu_admin()` maupun `menu_pelanggan()`.

---

## 5. Alur Admin

```text
menu_admin()
  |
  +-- login_admin()
  |     |-- username = "admin" dan password = "admin123" --> berhasil
  |     `-- salah --> ulang, maksimal 3 kali --> gagal, kembali ke menu utama
  |
  `-- while jalan:
        |-- "1" --> admin_lihat_menu()
        |-- "2" --> admin_tambah_menu()
        |-- "3" --> admin_ubah_menu()
        |-- "4" --> admin_hapus_menu()
        |-- "5" --> jalan = False --> logout
        `-- pilihan lain --> "Pilihan tidak valid!"
```

### 5.1 Menambah menu

Input yang diminta: nama, kategori (`1` = Makanan, `2` = Minuman), harga, dan stok. ID baru ditentukan dengan perulangan `for` atas kunci `menu`, lalu nilai terbesar ditambah satu.

### 5.2 Mengubah menu

Data lama ditampilkan sebagai panduan. Jika kolom dikosongkan, nilai lama dipertahankan. Kategori hanya boleh kosong, `"1"`, atau `"2"`. Harga harus lebih dari `0` dan stok tidak boleh negatif.

### 5.3 Menghapus menu

Setelah ID ditemukan, program meminta konfirmasi `y/n`. Jika dikonfirmasi, data dihapus dari `menu` dan dari `keranjang` memakai `pop()`.

> Pilihan `"1"` sampai `"4"` disimpan dalam dictionary `aksi` dan dipanggil dengan `aksi[pilih]()`. Cara ini menggantikan `elif`.

---

## 6. Alur Pelanggan

```text
menu_pelanggan()  -- while jalan:
  |
  +-- "1" --> pelanggan_pesan()
  |             |-- tampilkan menu
  |             |-- input ID, 0 = batal
  |             |-- cek ketersediaan menu dan stok
  |             |-- input jumlah pesanan
  |             |-- cek total qty terhadap stok
  |             `-- simpan ke keranjang
  |
  +-- "2" --> pelanggan_lihat_keranjang()
  +-- "3" --> pelanggan_hapus_keranjang()
  +-- "4" --> pelanggan_checkout()
  +-- "5" --> konfirmasi pengosongan keranjang --> keluar
  `-- pilihan lain --> "Pilihan tidak valid!"
```

### 6.1 Memesan

Jumlah pesanan ditambahkan dengan jumlah lama pada ID yang sama. Pesanan ditolak jika totalnya melebihi stok menu.

### 6.2 Menghapus item

Nomor urut diubah menjadi kunci dictionary dengan `list(keranjang.keys())[no - 1]`, kemudian item dihapus memakai `pop()`.

### 6.3 Kembali ke menu utama

Jika keranjang masih berisi, program bertanya dahulu sebelum mengosongkannya. Jika keranjang kosong, program langsung kembali.

---

## 7. Alur Checkout dan Struk

```text
pelanggan_checkout()
  |
  +-- keranjang kosong --> berhenti
  +-- hitung total dari pelanggan_lihat_keranjang()
  +-- tampilkan metode pembayaran
  +-- pilih metode --> metode = pembayaran[pilih - 1]
  +-- jika "Tunai" --> input uang dibayarkan, minimal sama dengan total
  +-- kembalian = bayar - total
  |
  `-- konfirmasi "y/n"
        |-- "y" --> kurangi stok --> cetak_struk() --> keranjang.clear()
        `-- "n" --> dibatalkan, keranjang tetap tersimpan
```

### 7.1 Isi struk

1. Nomor struk acak: `random.randint(1000, 9999)`
2. Tanggal: `time.strftime("%d-%m-%Y")`
3. Jam: `time.strftime("%H:%M:%S")`
4. Identitas toko, nomor struk, tanggal, jam, kasir, dan metode bayar
5. Rincian item: nama, harga × jumlah = subtotal
6. Jumlah item, subtotal, diskon, total, dibayar, dan kembalian
7. Ucapan terima kasih

---

## 8. Aturan Validasi Input

| Bagian            | Aturan                                                                                |
| ----------------- | ------------------------------------------------------------------------------------- |
| `cek_angka(teks)` | Teks tidak kosong dan seluruh karakternya termasuk `0` sampai `9`                     |
| `input_angka()`   | Nilai harus angka, minimal `min_val`, dan maksimal `max_val` jika tidak bernilai `-1` |
| `input_teks()`    | Nilai tidak boleh kosong setelah `strip()`                                            |
| `login_admin()`   | Username `admin`, password `admin123`, tiga kali percobaan                            |
| Kategori menu     | Hanya kosong, `"1"`, atau `"2"`                                                       |
| Harga dan stok    | Harga lebih dari `0`, stok minimal `0`                                                |
| Pembayaran tunai  | Uang dibayarkan minimal sama dengan total belanja                                     |

Input yang tidak sesuai memicu perulangan `while True` untuk menanyakan kembali nilai tersebut.

---

## 9. Cara Menjalankan

```bash
cd "D:\Document\Algoritma & Dasar Pemrograman\project"
python tugasakhirgpt.py
```

Contoh alur singkat:

```text
2  -> masuk sebagai pelanggan
1  -> pilih "Masukkan Pesanan ke Keranjang"
1  -> ID menu Nasi Goreng
1  -> jumlah pesanan
4  -> checkout
1  -> metode Tunai
20000 -> uang dibayarkan
y  -> konfirmasi pesanan
5  -> kembali ke menu utama
3  -> keluar program
```

---

## 10. Catatan Tambahan

- Data menu, keranjang, dan stok tersimpan di memori. Menutup program mengembalikan data ke kondisi awal.
- Nomor struk bersifat acak sehingga memungkinkan angka yang sama pada dua transaksi. Jika ingin nomor unik, nomor yang sudah dipakai dapat disimpan dalam list lalu dicek memakai operator `in`.
- Tanggal dan jam mengikuti waktu lokal komputer yang menjalankan program.
- Program telah diperiksa dengan `python -m py_compile tugasakhirgpt.py`, dan alur pesan → checkout → struk berjalan tanpa error.
