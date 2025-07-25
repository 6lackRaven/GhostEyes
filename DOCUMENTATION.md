# GhostEyes v2.1.0 — Full Documentation

**Author:** 6lackRaven  
**License:** MIT  
**Version:** 2.1.0  
**Status:** Stable (Async-first)

---

## 📖 Overview

**GhostEyes** is a modular, async-powered **offensive reconnaissance toolkit** designed for **penetration testers** and **red teamers**.  
It combines **network scanning**, **web reconnaissance**, and **report generation** in one unified tool.

Key principles:
- **Fast:** Async I/O for high concurrency.
- **Modular:** Easily extensible with new modules.
- **Cross-domain:** Supports both **network-layer** and **web-layer** recon.
- **Auditable:** Generates **reports** in multiple formats (HTML, JSON, TXT, CSV).

---

## ⚙️ Installation

### Requirements
- **Python 3.10+** (3.12+ recommended)
- `pip install -r requirements.txt`
- Root privileges (for raw packet operations with Scapy)

### Install Steps
```bash
git clone https://github.com/6lackRaven/GhostEyes.git
cd GhostEyes
pip install -r requirements.txt
```

---

🎯 Commands Overview

Command	Purpose

net	Network reconnaissance
web	Web reconnaissance
report	Generate multi-format reports
-h/--help	Show help for any command
--version	Show current version and author info
--examples	Display common usage examples



---

🧭 Global Flags

Flag	Description

-h, --help	Show all commands and usage details
--version	Show version (e.g., GhostEyes v2.1.0 by 6lackRaven)
--examples	Display ready-to-use command examples
--quiet	Reduce verbosity (only show critical results)



---

🔍 Network Reconnaissance (net)

Syntax:

python ghosteyes.py net -i <interface> [OPTIONS]

Options:

Option	Description

-i, --interface	Network interface (e.g., eth0, wlan0)
-s, --scan CIDR	ARP-based subnet scanning
-v, --vlan	Discover VLANs
-t, --track	Track live devices in real time
-r, --trace IP	Layer 2 traceroute to a target
-d, --dhcp	Capture DHCP traffic
--duration N	Duration for vlan/track/dhcp (default: 300s)
--output FILE	Save results (default: scan_net.json)


Examples:

# Basic ARP scan
sudo python ghosteyes.py net -i eth0 --scan 192.168.1.0/24

# VLAN discovery for 60s
sudo python ghosteyes.py net -i eth0 --vlan --duration 60

# Track devices (quiet mode)
sudo python ghosteyes.py net -i wlan0 --track --quiet

How It Works

ARP Scan: Crafts ARP requests to identify active hosts.

VLAN Discovery: Uses VLAN tagging/sniffing to identify VLANs on the network.

Device Tracking: Continuously monitors ARP responses and MAC changes.

Layer 2 Traceroute: Uses ARP requests to map hops at Layer 2.

DHCP Snooping: Captures DHCP ACK/REQUEST packets to log leases.



---

🌐 Web Reconnaissance (web)

Syntax:

python ghosteyes.py web -u <URL> [OPTIONS]

Options:

Option	Description

-u, --url	Target URL (e.g., https://example.com)
-s, --subdomains	Subdomain brute-force (wordlist required)
-b, --bruteforce	Directory brute-force (wordlist required)
-T, --tech	Detect web technology stack
-w, --workers N	Concurrent workers (default: 50)
--output FILE	Save results (default: scan_web.json)


Examples:

# Subdomain enumeration + tech detection
python ghosteyes.py web -u https://example.com -s subdomains.txt -T

# Directory brute-force
python ghosteyes.py web -u https://example.com -b dirs.txt

# Full scan with custom workers
python ghosteyes.py web -u https://example.com -s subdomains.txt -b dirs.txt -T -w 100

How It Works

Uses async HTTP requests for fast scanning.

Parses subdomains from DNS responses.

Detects technologies via fingerprinting (headers, responses, favicon hashes).

Supports custom wordlists for brute-force attacks.



---

📑 Report Generation (report)

Syntax:

python ghosteyes.py report -f <JSON_FILE> -t [txt|json|html|csv|all]

Examples:

# Generate HTML report
python ghosteyes.py report -f scan_net.json -t html

# Generate all formats
python ghosteyes.py report -f scan_web.json -t all

Reports are saved automatically to the reports/ folder with timestamps.


---

🔧 Advanced Features

1. Colorized Output:
Errors, warnings, and success messages are color-coded for clarity.


2. Async Engine:
All heavy operations (scans, web requests) are handled asynchronously, ensuring speed.


3. Quiet Mode (--quiet):
Only displays essential output (ideal for automation).


4. Auto-Save JSON:
Each scan automatically saves raw data to scan_<module>.json.




---

🗺️ Roadmap (Future v3)

Plugin-based module system.

Config file (ghosteyes.toml) for persistent settings.

REST API + Web Dashboard for scans.

Auto-update functionality.

Parallel TCP port scanning.



---

⚠️ Legal & Ethical Usage

GhostEyes is only for authorized security testing.
Do NOT use it on networks or websites you do not own or have permission to test.


---

📝 Changelog Highlights (v2.1.0)

Added colorized banner and CLI improvements.

Added --examples flag for quick usage reference.

Fixed asyncio.run() event loop conflict (safer async).

Added directory brute-force feature.

Improved help system and user experience.



---

📬 Contact & Support

Author: 6lackRaven
Email:  harleystanislas.raven@gmail.com
Telegram: Thereal6lackRaven
Facebook: Harley Stanislas

For bug reports: GitHub Issues


