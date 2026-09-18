from pwn import *

m = "6f636970"

data = unhex(m)

print(data.decode())
