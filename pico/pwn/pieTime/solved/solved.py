

# program for automatically calculating hexadecimal operations

hexa1 = input("enter first hexadecimal number\n")

operator = input("enter the operator (+/-)\n")

hexa2 = input("enter second hexadecimal number\n")

match operator:
    case "+":
        output = int(hexa1, 16) + int(hexa2, 16)
    case "-":
        output = int(hexa1, 16) - int(hexa2, 16)
        
    case _:
        output = "error"

print(hex(output))