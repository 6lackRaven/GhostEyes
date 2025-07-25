# GhostEyes v2.1.0 — Offensive Reconnaissance Toolkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-v2.1.0-green.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/6lackRaven/GhostEyes?style=social)](https://github.com/6lackRaven/GhostEyes)

> **Author:** 6lackRaven  
> **Status:** Active • Stable • Async-first  
> **Docs:** See [`DOCUMENTATION.md`](DOCUMENTATION.md) • Changelog in [`CHANGELOG.md`](CHANGELOG.md)

---

## 🧠 What is GhostEyes?

**GhostEyes** is an async-first, modular **offensive reconnaissance toolkit** for **network** and **web** recon, plus **report generation** — designed for penetration testers, red teams, and researchers.

- **No nested `asyncio.run()` errors** – fixed in v2.1.0  
- **Colorized CLI**, **quiet mode**, **custom output path**, and **examples flag**
- Clean codebase, ready for further v3 refactors (plugins, structured logs, etc.)

---

## ✨ Key Features

- **Network Recon**
  - ARP subnet scanning
  - VLAN discovery & sampling
  - Layer 2 traceroute
  - DHCP snooping
  - Real-time device tracking

- **Web Recon**
  - Subdomain brute-force
  - Directory brute-force
  - Technology stack detection

- **Reports**
  - Generate **TXT / JSON / HTML / CSV** from prior scans

- **CLI UX**
  - `--version`, `--examples`, `--quiet`, `--output`
  - Colorized output
  - One single `asyncio.run()` (no runtime loop conflicts)

---

## 📦 Installation

```bash
git clone https://github.com/6lackRaven/GhostEyes.git
cd GhostEyes
pip install -r requirements.txt
```


Python 3.10+ recommended.


---

🚀 Quick Start

# Show help
python ghosteyes.py -h

# Show version
python ghosteyes.py --version

# Show practical examples
python ghosteyes.py --examples


---

⚙️ Commands & Flags

Global Flags

Flag	Description

- --version	Show version and author, then exit
- --examples	Show common usage examples
- --quiet	Suppress verbose logs



---

net — Network Reconnaissance

Usage:

python ghosteyes.py net -i <iface> [--scan CIDR | --vlan | --track | --trace IP | --dhcp] [--duration N] [--output FILE]

Options:

Option	Description

- -i, --interface	Network interface (default: eth0)
- -s, --scan CIDR	ARP scan a subnet (e.g., 192.168.1.0/24)
- -v, --vlan	Discover VLANs
- -t, --track	Track live devices
- -r, --trace IP	Layer 2 traceroute to target
- -d, --dhcp	Capture DHCP traffic
- --duration N	Duration in seconds for vlan/track/dhcp (default: 300)
- --output FILE	Where to save results (default: scan_net.json)


Examples:

# ARP scan
python ghosteyes.py net -i eth0 --scan 192.168.1.0/24 --output my_scan.json

# VLAN discovery (2 minutes)
python ghosteyes.py net -i eth0 --vlan --duration 120

# Track devices (quiet mode)
python ghosteyes.py net -i wlan0 --track --duration 60 --quiet


---

web — Web Reconnaissance

Usage:

python ghosteyes.py web -u <url> [-s WORDLIST] [-b WORDLIST] [-T] [-w N] [--output FILE]

Options:

Option	Description

- -u, --url	Target URL (required)
- -s, --subdomains	Subdomain brute-force wordlist
- -b, --bruteforce	Directory brute-force wordlist
- -T, --tech	Detect technology stack
- -w, --workers	Number of concurrent workers (default: 50)
- --output FILE	Where to save results (default: scan_web.json)


Examples:

# Subdomain scan + tech detection
python ghosteyes.py web -u https://example.com -s subdomains.txt -T

# Directory brute-force (quiet mode)
python ghosteyes.py web -u https://example.com -b dirs.txt --quiet


---

report — Report Generation

Usage:

python ghosteyes.py report -f scan_net.json -t html json

Options:

Option	Description

- -f, --file	Input scan results file (JSON)
- -t, --type	Output formats: txt, json, html, csv, or all


Examples:

# HTML + JSON output
python ghosteyes.py report -f scan_net.json -t html json

# Everything
python ghosteyes.py report -f scan_web.json -t all


---

📂 Output

Unless overridden via --output, scans are saved to:

scan_net.json for net

scan_web.json for web



---

🗺️ Roadmap (towards v3)

Plugin system & runtime module discovery

Structured JSON logging and log levels

Config file support (ghosteyes.toml / YAML)

Parallelized scans with cancellation and timeouts

Packaging (pip install ghosteyes) & self-contained binaries

REST API / Web UI


Read more in CHANGELOG.md.


---

⚠️ Legal & Ethical Disclaimer

GhostEyes is intended strictly for authorized security testing and educational use.
By using this tool, you accept full responsibility for your actions.

Only scan targets you own or have explicit written permission to test.

Comply with applicable laws (e.g., CFAA, GDPR).

The author(s) are not liable for misuse or damage.



---

📜 License

MIT — see the LICENSE file.


---

💬 Contact

- Author: 6lackRaven
- Email:  harleystanislas.raven@gmail.com
- Telegram: Thereal6lackRaven
- Facebook: Harley Stanislas


---

🤝 Contributing

Contributions are welcome!

1. Fork the repo


2. Create a feature branch: git checkout -b feature/your-feature


3. Commit clean, tested code


4. Open a PR with a clear description



Please follow the established code style & be respectful.


---

❤️ Support / Donations

If you’d like to support continued open-source development:

- Bitcoin (BTC):   bc1qvc8y7z2jguzr7e3fvwyf09l3me94mqk06nz3hj
- Ethereum (ETH):  0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15
- USDT (ERC20):    0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15
- BNB (BEP20):     0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15
- Solana (SOL):    E7x7ak3H6ob2eHbgsbfgVXpEJyVqMPUFPBtkuEUKj2cq

Thank you for supporting independent security tooling 🙏

