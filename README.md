# GhostEyes v2 - Offensive Reconnaissance Toolkit

![GhostEyes Logo](https://i.imgur.com/ghosteyes_logo.png)

Advanced cybersecurity toolkit for network reconnaissance, vulnerability discovery, and penetration testing.

## Features
- Network scanning & host discovery
- VLAN hopping & Layer 2 attacks
- Web reconnaissance (subdomains, directories, tech stack)
- Real-time device tracking
- Multi-format reporting

## Installation
```bash
git clone https://github.com/6lackRaven/GhostEyes.git
cd GhostEyes
pip install -r requirements.txt

## Usage

# Network scanning
sudo ./ghosteyes.py net --scan 192.168.1.0/24

# VLAN discovery
sudo ./ghosteyes.py net --vlan --duration 60

# Web reconnaissance
./ghosteyes.py web --url https://example.com --tech

# Generate reports
./ghosteyes.py report --file scan_web.json --type html

## Modules
Command | Function |
|---------|----------|
| `net --scan` | ARP subnet scanning |
| `net --vlan` | VLAN discovery |
| `net --trace` | Layer 2 traceroute |
| `web --subdomains` | Subdomain enumeration |
| `web --bruteforce` | Directory brute-forcing |

## Disclaimer

## LEGAL NOTICE
GhostEyes is developed for **AUTHORIZED SECURITY TESTING AND LEGITIMATE EDUCATIONAL PURPOSES ONLY**.

🚨 **WARNING: UNAUTHORIZED USE IS ILLEGAL**
- You must have explicit written permission to scan or test any network or system
- You are solely liable for any misuse of this toolkit
- Developers assume no responsibility for unauthorized or illegal use

## ETHICAL GUIDELINES
1. **Always obtain proper authorization** before using GhostEyes
2. **Never target systems** you don't own or have permission to test
3. **Respect privacy** - Do not access or collect personal data
4. **Comply with all applicable laws** (Computer Fraud and Abuse Act, GDPR, etc.)

## PROFESSIONAL USE
GhostEyes should only be used by:
- Certified security professionals
- Penetration testers with valid contracts
- Security researchers with explicit permissions
- Educational institutions in controlled environments

By using this software, you acknowledge that:
- You understand these terms
- You accept full liability for your actions
- The developers bear no responsibility for misuse
