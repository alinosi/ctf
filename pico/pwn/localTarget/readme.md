65 has byte 0x41.

'A' has same byte because the format encoding(utf8) define 'A' as 65.


memory doesn't gave a shit, it just understand bit, bit is number, so 'A' must be have number form to allowed memory space.

so before 'A' getting place in memory, the compiler proccess it into hex following the encoding format(utf-8).
so 'A' has 'number form' now. after that, compiler translate it into binary form(we can assume it as hex). As we say it before, 65 in hex is 0x41,
so the conditons ( number == 65) has been fulfilled. In more technical form, it's like (0x41 == 0x41) or (01000001 == 01000001)
