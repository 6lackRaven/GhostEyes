from scapy.all import srp, Ether, ARP, conf
from core.utils import TraceHop, mac_vendor_lookup
import asyncio

class Layer2Traceroute:
    def __init__(self, interface: str):
        conf.iface = interface
        self.interface = interface
    
    async def trace(self, target_ip: str, max_hops: int = 15) -> list:
        path = []
        current_hop = 0
        dst_mac = None
        
        while current_hop < max_hops:
            current_hop += 1
            
            # Craft probe with increasing TTL
            arp_probe = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(
                pdst=target_ip, 
                hwdst=dst_mac or "ff:ff:ff:ff:ff:ff",
                hlim=current_hop
            )
            
            # Send and wait for response
            ans, _ = srp(arp_probe, timeout=2, verbose=False)
            
            if not ans:
                path.append(TraceHop(current_hop, "Timeout", "", ""))
                continue
                
            # Process response
            response = ans[0][1]
            hop_ip = response.psrc
            hop_mac = response.hwsrc
            vendor = await mac_vendor_lookup(hop_mac)
            
            path.append(TraceHop(current_hop, hop_mac, hop_ip, vendor))
            
            # Update next hop MAC
            dst_mac = hop_mac
            
            # Stop if target reached
            if hop_ip == target_ip:
                break
                
        return path
