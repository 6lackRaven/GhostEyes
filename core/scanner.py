import asyncio
import socket
import struct
from scapy.all import srp, sr1, conf
from .packet_crafter import PacketCrafter
from .utils import validate_cidr, get_interface_details

class NetworkScanner:
    def __init__(self, interface: str = "eth0"):
        self.interface = interface
        conf.iface = interface
        self.crafter = PacketCrafter(interface)
        self.local_info = asyncio.run(get_interface_details(interface))
    
    async def arp_scan(self, subnet: str) -> list:
        if not validate_cidr(subnet):
            raise ValueError(f"Invalid CIDR: {subnet}")
        
        arp_pkt = self.crafter.craft_arp(
            src_ip=self.local_info.ip,
            dst_ip=subnet.split('/')[0],
            opcode=1
        )
        
        result = srp(arp_pkt, timeout=2, verbose=False)[0]
        return [{'ip': rcvd.psrc, 'mac': rcvd.hwsrc} for _, rcvd in result]
    
    async def icmp_ping_sweep(self, ip_range: list, timeout: int = 1) -> list:
        alive_hosts = []
        for ip in ip_range:
            pkt = self.crafter.craft_icmp_echo(ip)
            response = sr1(pkt, timeout=timeout, verbose=False)
            if response:
                alive_hosts.append(ip)
        return alive_hosts
    
    async def tcp_port_scan(self, target: str, ports: list) -> dict:
        open_ports = {}
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports[port] = "open"
            sock.close()
        return open_ports
