from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP, ICMP
from scapy.layers.l2 import ARP, Ether, Dot1Q
from .utils import validate_ip

class PacketCrafter:
    def __init__(self, interface: str):
        self.interface = interface
        self.local_mac = get_if_hwaddr(interface)
    
    def craft_arp(self, src_ip: str, dst_ip: str, opcode: int, 
                 vlan: int = None) -> Ether:
        eth = Ether(src=self.local_mac, dst="ff:ff:ff:ff:ff:ff")
        if vlan:
            eth /= Dot1Q(vlan=vlan)
        return eth / ARP(op=opcode, psrc=src_ip, pdst=dst_ip)
    
    def craft_dhcp_discover(self, vlan: int = None) -> Ether:
        eth = Ether(src=self.local_mac, dst="ff:ff:ff:ff:ff:ff")
        if vlan:
            eth /= Dot1Q(vlan=vlan)
        return (eth /
                IP(src="0.0.0.0", dst="255.255.255.255") /
                UDP(sport=68, dport=67) /
                BOOTP(chaddr=[mac2str(self.local_mac)]) /
                DHCP(options=[("message-type", "discover"), "end"]))
    
    def craft_icmp_echo(self, dst_ip: str, ttl: int = 64) -> IP:
        return IP(dst=dst_ip, ttl=ttl) / ICMP()
    
    def craft_l2_probe(self, dst_mac: str) -> Ether:
        return Ether(src=self.local_mac, dst=dst_mac) / ARP(op="who-has")
