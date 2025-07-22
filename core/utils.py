import re
import asyncio
import netifaces
import requests
from collections import namedtuple

# Data structures
NetworkInterface = namedtuple('NetworkInterface', ['name', 'ip', 'mac', 'netmask'])
VLANResult = namedtuple('VLANResult', ['id', 'devices'])
TraceHop = namedtuple('TraceHop', ['hop', 'mac', 'ip', 'vendor'])

def validate_ip(ip: str) -> bool:
    pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    return re.match(pattern, ip) is not None

def validate_cidr(subnet: str) -> bool:
    cidr_pattern = r"^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$"
    if not re.match(cidr_pattern, subnet):
        return False
    ip, mask = subnet.split('/')
    return validate_ip(ip) and 0 <= int(mask) <= 32

async def get_interface_details(interface: str) -> NetworkInterface:
    addrs = netifaces.ifaddresses(interface)
    ip = addrs[netifaces.AF_INET][0]['addr']
    mac = addrs[netifaces.AF_LINK][0]['addr']
    netmask = addrs[netifaces.AF_INET][0]['netmask']
    return NetworkInterface(interface, ip, mac, netmask)

async def mac_vendor_lookup(mac: str) -> str:
    oui = mac[:8].replace(':', '').upper()
    try:
        response = requests.get(f"https://api.macvendors.com/{oui}", timeout=2)
        return response.text if response.status_code == 200 else "Unknown"
    except:
        return "Unknown"
