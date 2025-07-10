# 👁️ GhostEyes

**GhostEyes** is a powerful, beginner-friendly Python CLI port scanner  
created by [6lackRaven](https://github.com/6lackRaven).  
Fast, clean, and perfect for hackers, sysadmins, or learners.

---

## ⚙️ Features

- Multi-threaded scanning
- Service detection (HTTP, SSH, MySQL, etc.)
- Auto hostname + IP info
- Scan time tracking
- Easy CLI — no complex flags
- ASCII logo branding

---

## 🚀 Usage

```bash
# Default scan (ports 1–1024)
python3 ghosteyes.py 192.168.1.1

# Custom range
python3 ghosteyes.py scanme.nmap.org --start 20 --end 8888

# More threads
python3 ghosteyes.py example.com --threads 200


---

## ⚠️ Disclaimer

GhostEyes is intended **for educational and authorized testing purposes only**.  
Do not use this tool on networks or systems you do not own or have explicit permission to scan.  

The developer **(6lackRaven)** is not responsible for any misuse or damage caused by this tool.
Use responsibly. 🚨
