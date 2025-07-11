# 👁️ GhostEyes - Advanced Python Port Scanner

GhostEyes is a powerful, beginner-friendly **Python-based port scanner** designed for ethical hacking, penetration testing, and network diagnostics. It supports fast threaded scans, banner grabbing, OS detection, and web tech fingerprinting.

> 🔒 For **educational and ethical use only**.

---

## 🚀 Features

- ✅ **Multithreaded TCP Port Scanning**
- ✅ **Banner Grabbing** (on open ports)
- ✅ **OS Detection** (based on TTL fingerprinting)
- ✅ **Web Technology Fingerprinting** (`Server`, `X-Powered-By`)
- ✅ **Common Service Mapping**
- ✅ **Fast with Thread Support**
- ✅ **Output Saving to File**
- ✅ User-friendly CLI

---

## 📦 Installation

```bash
git clone https://github.com/6lackRaven/GhostEyes.git
cd GhostEyes
pip install -r requirements.txt


---

## 📌 Usage

python3 scan.py <target> [options]

## 🔧 Example

python3 scan.py scanme.nmap.org --start 1 --end 100 --threads 100 --mode banner --detect --output result.txt


---

## 🛠️ Options

Option	Description

<target>	Target IP or domain
--start	Start port (default: 1)
--end	End port (default: 1024)
--threads	Number of threads (default: 100)
--mode	basic (default) or banner mode
--detect	Enable OS & Web tech fingerprinting
--output	Save results to a file



---

## 🔍 What It Detects

Open TCP ports (1–65535)

Banner info from services (if any)

Server and backend framework (via HTTP headers)

OS fingerprinting from TTL analysis (basic)



---

## 📁 Output

If --output result.txt is specified, the open ports and services will be saved to a .txt file.


---

## 🧠 How It Works

Connects to each port via TCP (multi-threaded)

Grabs banners from open ports

Uses TTL to guess operating system (e.g. Linux vs Windows)

Sends HTTP requests to detect backend tech via headers



---

## ⚠️ Disclaimer

This tool is built for learning and ethical testing only. Do not scan networks without permission.

