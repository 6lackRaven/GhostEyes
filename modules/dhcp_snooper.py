from scapy.all import sniff, DHCP, BOOTP, Ether
from scapy.data import ETH_P_ALL

class DHCPSnooper:
    def __init__(self, interface: str):
        self.interface = interface
        self.leases = {}
    
    async def capture_dhcp(self, duration: int = 60):
        def packet_handler(pkt):
            if DHCP in pkt:
                mac = pkt[Ether].src
                message_type = pkt[DHCP].options[0][1]
                
                if message_type == 1:  # DHCP Discover
                    self.leases[mac] = {'state': 'discovering'}
                    
                elif message_type == 2:  # DHCP Offer
                    if mac in self.leases:
                        self.leases[mac]['server'] = pkt[IP].src
                        self.leases[mac]['offered_ip'] = pkt[BOOTP].yiaddr
                
                elif message_type == 3:  # DHCP Request
                    if mac in self.leases:
                        self.leases[mac]['state'] = 'requesting'
                
                elif message_type == 5:  # DHCP ACK
                    if mac in self.leases:
                        self.leases[mac]['ip'] = pkt[BOOTP].yiaddr
                        self.leases[mac]['subnet'] = next(
                            (opt[1] for opt in pkt[DHCP].options if opt[0] == 'subnet_mask'), 
                            None
                        )
                        self.leases[mac]['router'] = next(
                            (opt[1] for opt in pkt[DHCP].options if opt[0] == 'router'),
                            None
                        )
                        self.leases[mac]['lease_time'] = next(
                            (opt[1] for opt in pkt[DHCP].options if opt[0] == 'lease_time'),
                            None
                        )
                        self.leases[mac]['state'] = 'leased'
        
        sniff(prn=packet_handler, timeout=duration, 
              filter="port 67 or port 68", store=False, 
              iface=self.interface)
