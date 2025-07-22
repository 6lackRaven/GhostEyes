import socket
import threading
import argparse
import platform
import time
import requests
import string
from queue import Queue
from datetime import datetime
from pyfiglet import Figlet

# Global variables
queue = Queue()
open_ports = []

common_services = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-ALT",
}

def print_banner():
    fig = Figlet(font='slant')
    print(fig.renderText('GhostEyes'))
    print("[*] GhostEyes - Port Scanner Tool")
    print("[*] by 6lackRaven")
    print("-" * 60)

def clean_banner(raw_banner):
    return ''.join(c if c.isprintable() else '.' for c in raw_banner)

def portscan(target, port, mode):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((target, port)) == 0:
                banner = ""
                if mode == "banner":
                    try:
                        s.send(b"\r\n")
                        banner_bytes = s.recv(1024)
                        banner = banner_bytes.decode(errors="ignore").strip()
                        banner = clean_banner(banner)
                    except:
                        banner = "No banner"
                service = common_services.get(port, "Unknown")
                result = f"[+] Port {port} open ({service})"
                if mode == "banner":
                    result += f" - {banner}"
                print(result)
                open_ports.append((port, f"{service} | {banner}" if banner else service))
    except:
        pass

def worker(target, mode):
    while not queue.empty():
        port = queue.get()
        portscan(target, port, mode)
        queue.task_done()

def fill_queue(start, end):
    for port in range(start, end + 1):
        queue.put(port)

def system_info(target):
    print("[*] Target Info")
    try:
        hostname = socket.gethostbyaddr(target)[0]
    except:
        hostname = "Unknown"
    print(f"[+] Target IP     : {target}")
    print(f"[+] Hostname      : {hostname}")
    print(f"[+] Your OS       : {platform.system()} {platform.release()}")
    print(f"[+] Start Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

def os_detection(target):
    print("[*] OS Detection (Basic Fingerprinting)")
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
            print(f"[+] TTL={ttl} => Likely OS: {os_guess}")
    except:
        print("[!] Could not perform OS detection.")

def tech_fingerprint(target):
    print("[*] Web Tech Fingerprinting")
    try:
        response = requests.get(f"http://{target}", timeout=3)
        headers = response.headers
        server = headers.get("Server", "Unknown")
        powered_by = headers.get("X-Powered-By", "Unknown")
        print(f"[+] Server        : {server}")
        print(f"[+] X-Powered-By  : {powered_by}")
    except:
        print("[!] Could not detect web technologies.")

def save_results(output_file, target_ip):
    try:
        with open(output_file, "w") as f:
            f.write(f"Open Ports on {target_ip}:\n")
            for port, service in sorted(open_ports):
                f.write(f"Port {port}: {service}\n")
        print(f"[+] Results saved to {output_file}")
    except Exception as e:
        print(f"[!] Failed to save results: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="GhostEyes - Port Scanner Tool",
        epilog="Example: python3 ghosteyes.py 192.168.1.1 --start 1 --end 1000 --mode banner --output scan.txt"
    )
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("--threads", type=int, default=100, help="Thread count (default: 100)")
    parser.add_argument("--output", help="Save scan result to file")
    parser.add_argument("--mode", choices=["basic", "banner"], default="basic", help="Scan mode")
    parser.add_argument("--detect", action="store_true", help="Enable OS and tech fingerprinting")
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("[!] Error: Could not resolve target.")
        return

    print_banner()
    system_info(target_ip)
    fill_queue(args.start, args.end)

    start_time = time.time()

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(target_ip, args.mode))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    duration = time.time() - start_time
    print("\n[*] Scan Complete")

    if open_ports:
        print(f"[+] Open Ports on {target_ip}:")
        for port, service in sorted(open_ports):
            print(f"    - Port {port}: {service}")
        if args.output:
            save_results(args.output, target_ip)
    else:
        print("[!] No open ports found.")

    print(f"[+] Duration: {duration:.2f} seconds")

    if args.detect:
        os_detection(target_ip)
        tech_fingerprint(target_ip)

if __name__ == "__main__":
    main()
