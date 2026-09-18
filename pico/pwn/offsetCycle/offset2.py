from pwn import *
import sys

argument = sys.argv[1]

target_address = int(argument, 16)

raw_bytes = p32(target_address)

instructions = ["cyclic", "-l", raw_bytes]

try:
    results = subprocess.run(instructions, capture_output=True, check=True)
    print("offset: ")
    print(results.stdout.decode('utf-8'))

except subprocess.CalledProcessError as e:
    print(f"Error while running {e}")
