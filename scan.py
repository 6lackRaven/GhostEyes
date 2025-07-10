#!/usr/bin/env python3

import socket
import threading
import argparse
import platform
import time
from queue import Queue
from datetime import datetime

# === GLOBAL ===
queue = Queue()
open_ports = []
common_services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-ALT",
}

# === ASCII BANNER ===
def print_banner():
    banner = r"""
   ____ _               _     ______           
  / ___| |__   ___  ___| |_  |  ____|   ___ ___ 
 | |  _| '_ \ / _ \/ __| __| | |_ / _ \ / __/ _ \
 | |_| | | | |  __/\__ \ |_  |  _| (_) | (_|  __/
  \____|_| |_|\___||___/\__| |_|  \___/ \___\___|

         👁️ GhostEyes - Port Scanner Tool
              by 6lackRaven
    """
    print(banner)

# === PORT SCANNER ===
def portscan(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = common_services.get(port, "Unknown")
                print(f"[+] Port {port} is open ({service})")
                open_ports.append((port, service))
    except:
        pass

# === THREAD WORKER ===
def worker(target):
    while not queue.empty():
        port = queue.get()
        portscan(target, port)

# === PORT QUEUE FILLER ===
def fill_queue(start, end):
    for port in range(start, end + 1):
        queue.put(port)

# === SYSTEM INFO ===
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

# === MAIN LOGIC ===
def main():
    parser = argparse.ArgumentParser(
        description="🛡️ PortXRay - Simple, Fast Python Port Scanner",
        epilog="Example: python3 portxray.py 192.168.0.1 --start 1 --end 1024 --threads 100"
    )
    parser.add_argument(
        "target", 
        help="Target IP address or domain name to scan (e.g. 192.168.1.1 or google.com)"
    )
    parser.add_argument(
        "--start", 
        type=int, 
        default=1, 
        help="Starting port number to scan (default: 1)"
    )
    parser.add_argument(
        "--end", 
        type=int, 
        default=1024, 
        help="Ending port number to scan (default: 1024)"
    )
    parser.add_argument(
        "--threads", 
        type=int, 
        default=100, 
        help="Number of threads to use (default: 100)"
    )
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("❌ Error: Could not resolve target address.")
        return

    print_banner()
    system_info(target_ip)
    fill_queue(args.start, args.end)

    start_time = time.time()  # Start timer

    thread_list = []
    for _ in range(args.threads):
        thread = threading.Thread(target=worker, args=(target_ip,))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    end_time = time.time()
    duration = end_time - start_time

    print("\n✅ Scan Complete")
    if open_ports:
        print(f"\n📖 Open Ports on {target_ip}:")
        for port, service in sorted(open_ports):
            print(f"  - Port {port}: {service}")
    else:
        print("❌ No open ports found.")

    print(f"\n⏱️ Scan Duration: {duration:.2f} seconds")

if __name__ == "__main__":
    main()
