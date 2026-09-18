# Method A (Returns bytes)
ascii_list = "42 72 7f 35 00 00 00 00 57 0d 00 a4 c8 c7 c3 da"

# Method B (Returns a Python string)
result = "".join([chr(i) for i in ascii_list])
print(result) # Output: Hello
