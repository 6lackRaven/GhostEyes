## GhostEyes v2 - Offensive Reconnaissance Toolkit

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-yellow)](https://github.com/6lackRaven/GhostEyes?tab=License-1-ov-file)
[![GitHub stars](https://img.shields.io/github/stars/6lackRaven/GhostEyes?style=social)](https://github.com/6lackRaven/GhostEyes)

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/202351661/469445619-d59c7e15-68e7-4b9b-9077-0dc9b0bce7d7.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTMzMzI1MzAsIm5iZiI6MTc1MzMzMjIzMCwicGF0aCI6Ii8yMDIzNTE2NjEvNDY5NDQ1NjE5LWQ1OWM3ZTE1LTY4ZTctNGI5Yi05MDc3LTBkYzliMGJjZTdkNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDcyNFQwNDQzNTBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mZWY0ZTA3NTRlNzk2ZTkxNzU4MWNjZGI5NTRlMWQ3MTFmMWRmZjZlZjI1NTNlYzA1ODI2NzMwMjBiNDJlMjBiJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.nJnK0tBCARaDry7etMekQubWmg-yGMiDLlBFvinCVqw" alt="GhostEyes Banner" />
</p>

---

**GhostEyes** is an advanced offensive cybersecurity toolkit built with Python.  
It is designed for **network reconnaissance**, **vulnerability discovery**, and **penetration testing** — all in one modular and powerful tool.

---

## 🚀 Features

- 🔍 Network scanning & host discovery  
- 🌐 Web reconnaissance (subdomains, directories, tech stack)  
- 🔁 VLAN hopping & Layer 2 attacks  
- 📡 Real-time device tracking  
- 📑 Multi-format report generation (HTML, JSON, etc.)

---

## 📦 Installation

```bash
git clone https://github.com/6lackRaven/GhostEyes.git
cd GhostEyes
pip install -r requirements.txt
```


---

## ⚙️ Usage Examples

🔗 Network Scanning
```
sudo ./ghosteyes.py net --scan 192.168.1.0/24
```

🧠 VLAN Discovery
```
sudo ./ghosteyes.py net --vlan --duration 60
```
🌐 Web Reconnaissance
```
./ghosteyes.py web --url https://example.com --tech
```
📝 Report Generation
```
./ghosteyes.py report --file scan_web.json --type html
```

---

## 🧩 Available Modules

Command	Description
```
net --scan	ARP-based subnet scanning
net --vlan	VLAN discovery and hopping
net --trace	Layer 2 traceroute
web --subdomains	Subdomain enumeration
web --bruteforce	Directory brute-forcing
```


---

## ⚠️ Disclaimer

LEGAL NOTICE

GhostEyes is strictly intended for authorized security testing and educational purposes only.


---

## 🚨 WARNING: UNAUTHORIZED USE IS ILLEGAL

- You must have explicit written permission to scan or test any network or system.

- You are solely responsible for how you use this toolkit.

- The developers are not liable for any misuse.



---

## ETHICAL USAGE GUIDELINES

1. Always obtain proper authorization before using GhostEyes.

2. Never target systems you do not own or have permission to test.

3. Respect privacy — do not access or collect personal data.

4. Comply with all applicable laws and regulations (e.g., CFAA, GDPR).




---

## 👨‍💻 For Professional Use Only

GhostEyes is intended for use by:

- Certified cybersecurity professionals

- Penetration testers with valid contracts

- Security researchers with explicit permission

- Educational institutions in controlled environments

---

## 📝 By using this tool, you confirm that:

1. You understand and accept these terms.

2. You take full responsibility for your actions.

3. The developers bear no responsibility for misuse.



---

## 📜 License

GhostEyes is licensed under the MIT License.
See the LICENSE file for full terms.


---

## 📬 Contact

If you have questions, feedback, or want to collaborate:
```
Email: harleystanislas.raven@gmail.com

Telegram: Thereal6lackRaven

Facebook: Harley Stanislas
```


---

## ❤️ Support the Project

You can support GhostEyes by:

- ⭐️ Starring the repository

- 🗣️ Sharing it with your network

- 🐛 Reporting issues or contributing improvements


---


## 🤝 Contribution

Thank you to everyone who has contributed to GhostEyes through issues, pull requests, and suggestions! Your support helps make this toolkit better and more reliable.

If you'd like to contribute, please:

1. Fork the repository

2. Create a new branch for your changes (git checkout -b feature/your-feature)

3. Make your changes with clear, concise commits

4. Test your changes to ensure they work correctly

5. Push your branch to your fork (git push origin feature/your-feature)

6. Open a Pull Request describing what you’ve done and why


Please follow the existing code style and be respectful in discussions.

All contributions, big or small, are appreciated!


---

## 💸 Crypto Donations (Anonymous Support)

If you find my tools helpful and want to support future development anonymously:
```
Bitcoin (BTC): bc1qvc8y7z2jguzr7e3fvwyf09l3me94mqk06nz3hj

Ethereum (ETH): 0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15

USDT (ERC20): 0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15

BNB (BEP20): 0x58bC732d4279321F1E4A8cA57eD2Ad16ed5A2e15

Solana (SOL): E7x7ak3H6ob2eHbgsbfgVXpEJyVqMPUFPBtkuEUKj2cq
```

🙏 Every contribution helps me build more open-source tools and share cybersecurity knowledge. Thank you!
