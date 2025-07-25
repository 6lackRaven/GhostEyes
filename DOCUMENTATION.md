# GhostEyes v2.1.0 - Offensive Reconnaissance Toolkit
Author: **6lackRaven**  
Version: **2.1.0**  
License: MIT

---

## Introduction
GhostEyes is an advanced offensive reconnaissance toolkit designed for **network scanning**, **web reconnaissance**, and **report generation**.  
It offers fast asynchronous scanning capabilities with user-friendly CLI commands.

---

## Installation
```bash
git clone https://github.com/6lackRaven/GhostEyes
cd GhostEyes
pip install -r requirements.txt
```

---


### Requirements
- Python 3.10+ (tested on Python 3.12)
- `pip install -r requirements.txt`

### Running GhostEyes
```bash
python ghosteyes.py [COMMAND] [OPTIONS]
```

---

Commands Overview

GhostEyes has 3 main commands:

1. net – Perform network reconnaissance (ARP scans, VLAN discovery, live device tracking).


2. web – Perform web reconnaissance (subdomains, directory brute-force, tech stack).


3. report – Generate reports from previous scan results.



Use -h or --help to get details for each command:

python ghosteyes.py net -h


---

Global Flags

Flag	Description

--version	Show version & author information.
--examples	Show common usage examples.
--quiet	Suppress verbose logs.



---

1. Network Reconnaissance

Subcommand: net

Available Options

Option	Description

-i, --interface	Network interface to use (default: eth0).
-s, --scan	ARP scan a subnet (e.g., 192.168.1.0/24).
-v, --vlan	Discover VLANs.
-t, --track	Track live devices (monitoring mode).
-r, --trace	Layer 2 traceroute to a target IP.
-d, --dhcp	Capture DHCP traffic.
--duration	Duration of operation in seconds (default: 300).
--output	Custom output JSON file.


Examples

# Scan a subnet for active hosts
python ghosteyes.py net -i eth0 --scan 192.168.0.0/24

# Discover VLANs for 2 minutes
python ghosteyes.py net -i eth0 --vlan --duration 120

# Track live devices
python ghosteyes.py net -i wlan0 --track --duration 60


---

2. Web Reconnaissance

Subcommand: web

Available Options

Option	Description

-u, --url	Target URL (required).
-s, --subdomains	Subdomain brute-force wordlist file.
-b, --bruteforce	Directory brute-force wordlist file.
-T, --tech	Detect technology stack of target site.
-w, --workers	Number of concurrent workers (default: 50).
--output	Custom output JSON file.


Examples

# Web reconnaissance with subdomain enumeration
python ghosteyes.py web -u https://example.com -s subdomains.txt

# Detect technologies and brute-force directories
python ghosteyes.py web -u https://example.com -b dirs.txt -T


---

3. Report Generation

Subcommand: report

Available Options

Option	Description

-f, --file	Input scan results file (JSON).
-t, --type	Output report formats (txt, json, html, csv, all).


Examples

# Generate HTML and JSON reports
python ghosteyes.py report -f scan_net.json -t html json

# Generate all report types
python ghosteyes.py report -f scan_web.json -t all


---

Output Files

By default, scan results are saved as:

scan_net.json for net scans

scan_web.json for web scans You can change the filename using the --output option.



---

Changelog

For the latest updates, see CHANGELOG.md.


