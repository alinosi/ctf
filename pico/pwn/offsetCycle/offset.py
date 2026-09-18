from pwn import *

argument = sys.argv[1:]
bytes = argument[0]

final_bytes = ""

for x in range(10):
	if x == 0 or x == 1:
		continue
	final_bytes += bytes[x]

raw_bytes = unhex(final_bytes)

instructions = ["cyclic", "-l", raw_bytes]

try:
    results = subprocess.run(instructions, capture_output=True, text=True, check=True)
    print("offset: ")
    print(results.stdout)

except subprocess.CalledProcessError as e:
    print(f"Error while running{e}")
    print(f"Error message: {e.stderr}")
