import asyncio
import time
from scapy.all import AsyncSniffer, ARP, Ether
from collections import defaultdict
from core.utils import mac_vendor_lookup

class DeviceTracker:
    def __init__(self, interface="eth0", refresh_interval=30):
        self.interface = interface
        self.refresh_interval = refresh_interval
        self.devices = defaultdict(dict)
        self.sniffer = None
        
    async def start_monitoring(self, duration=300):
        """Monitor network for device presence"""
        self.sniffer = AsyncSniffer(
            iface=self.interface,
            filter="arp",
            prn=self._packet_handler,
            store=False
        )
        self.sniffer.start()
        
        # Refresh device list periodically
        start_time = time.time()
        while time.time() - start_time < duration:
            await self._refresh_devices()
            await asyncio.sleep(self.refresh_interval)
            
        self.sniffer.stop()
        return dict(self.devices)
    
    def _packet_handler(self, pkt):
        """Process ARP packets to track devices"""
        if ARP in pkt:
            ip = pkt[ARP].psrc
            mac = pkt[ARP].hwsrc
            self.devices[mac]["ip"] = ip
            self.devices[mac]["last_seen"] = time.time()
    
    async def _refresh_devices(self):
        """Update device metadata"""
        for mac in list(self.devices.keys()):
            # Remove stale devices (> 5 mins inactive)
            if time.time() - self.devices[mac]["last_seen"] > 300:
                del self.devices[mac]
                continue
                
            # Add vendor information
            if "vendor" not in self.devices[mac]:
                self.devices[mac]["vendor"] = await mac_vendor_lookup(mac)
                
            # Track presence duration
            if "first_seen" not in self.devices[mac]:
                self.devices[mac]["first_seen"] = self.devices[mac]["last_seen"]
            self.devices[mac]["duration"] = time.time() - self.devices[mac]["first_seen"]
