import socket
import threading
import argparse
import platform
import time
import requests
from queue import Queue
from datetime import datetime

queue = Queue()
open_ports = []
common_services = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-ALT",
}

def print_banner():
    banner = r"""
   ____ _               _     ______
  / ___| |__   ___  ___| |_  |  ____|   ___ ___
 | |  _| '_ \ / _ \/ __| __| | |_ / _ \ / __/ _ \
 | |_| | | | |  __/\__ \ |_  |  _| (_) | (_|  __/
  \____|_| |_|\___||___/\__| |_|  \___/ \___\___|

         👁️ GhostEyes - Port Scanner Tool
         👨🏾‍💻 by 6lackRaven
    """
    print(banner)

def portscan(target, port, mode):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((target, port)) == 0:
                banner = ""
                if mode == "banner":
                    try:
                        banner = s.recv(1024).decode(errors="ignore").strip()
                    except:
                        banner = "No banner"
                service = common_services.get(port, "Unknown")
                print(f"[+] Port {port} open ({service}) {'- ' + banner if banner else ''}")
                open_ports.append((port, f"{service} | {banner}" if banner else service))
    except:
        pass

def worker(target, mode):
    while not queue.empty():
        port = queue.get()
        portscan(target, port, mode)

def fill_queue(start, end):
    for port in range(start, end + 1):
        queue.put(port)

def system_info(target):
    print("📡 Target Info:")
    try:
        hostname = socket.gethostbyaddr(target)[0]
    except:
        hostname = "Unknown"
    print(f"• Target IP     : {target}")
    print(f"• Hostname      : {hostname}")
    print(f"• Your OS       : {platform.system()} {platform.release()}")
    print(f"• Start Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

def os_detection(target):
    print("\n🧠 OS Detection (Basic Fingerprinting)")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((target, 80))
            ttl = s.getsockopt(socket.SOL_IP, socket.IP_TTL)
            if ttl >= 128:
                os_guess = "Windows"
            elif ttl >= 64:
                os_guess = "Linux/Unix"
            else:
                os_guess = "Unknown/Custom Device"
            print(f"🧩 TTL={ttl} → Likely OS: {os_guess}")
    except:
        print("⚠️ Could not perform OS detection.")

def tech_fingerprint(target):
    print("\n🕸️ Web Tech Fingerprinting")
    try:
        response = requests.get(f"http://{target}", timeout=3)
        headers = response.headers
        server = headers.get("Server", "Unknown")
        powered_by = headers.get("X-Powered-By", "Unknown")
        print(f"• Server        : {server}")
        print(f"• X-Powered-By  : {powered_by}")
    except:
        print("⚠️ Could not detect web technologies.")

def main():
    parser = argparse.ArgumentParser(
        description="👁️ GhostEyes - Full Python Port Scanner",
        epilog="Ex: python3 scan.py 192.168.1.1 --start 1 --end 1000 --mode banner --output result.txt"
    )
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")
    parser.add_argument("--threads", type=int, default=100, help="Thread count")
    parser.add_argument("--output", help="Save result to file")
    parser.add_argument("--mode", choices=["basic", "banner"], default="basic", help="Scan mode")
    parser.add_argument("--detect", action="store_true", help="Enable OS & web fingerprinting")
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("❌ Error: Could not resolve target.")
        return

    print_banner()
    system_info(target_ip)
    fill_queue(args.start, args.end)

    start = time.time()

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(target_ip, args.mode))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    duration = time.time() - start

    print("\n✅ Scan Complete")
    if open_ports:
        print(f"\n📖 Open Ports on {target_ip}:")
        for port, service in sorted(open_ports):
            print(f"  - Port {port}: {service}")
        if args.output:
            with open(args.output, "w") as f:
                for port, service in sorted(open_ports):
                    f.write(f"Port {port}: {service}\n")
            print(f"💾 Results saved to {args.output}")
    else:
        print("❌ No open ports found.")

    print(f"\n⏱️ Duration: {duration:.2f} seconds")

    if args.detect:
        os_detection(target_ip)
        tech_fingerprint(target_ip)

if __name__ == "__main__":
    main()
