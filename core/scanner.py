import asyncio
import socket
from typing import Iterable, Dict, List, Optional

from scapy.all import srp, sr1, conf  # type: ignore

from .packet_crafter import PacketCrafter
from .utils import validate_cidr, get_interface_details


class NetworkScanner:
    """
    Async-friendly wrapper around a few blocking primitives (Scapy, sockets).
    We DO NOT call asyncio.run() here. Either:
      - use `await NetworkScanner.build(interface)`  (preferred)
      - or pass `local_info` manually to the constructor.
    """

    def __init__(self, interface: str, local_info):
        self.interface = interface
        conf.iface = interface
        self.crafter = PacketCrafter(interface)
        self.local_info = local_info  # object returned by get_interface_details()

    # -------- constructors -------- #

    @classmethod
    async def build(cls, interface: str) -> "NetworkScanner":
        local_info = await get_interface_details(interface)
        return cls(interface, local_info)

    # -------- scans -------- #

    async def arp_scan(self, subnet: str) -> List[Dict[str, str]]:
        if not validate_cidr(subnet):
            raise ValueError(f"Invalid CIDR: {subnet}")

        arp_pkt = self.crafter.craft_arp(
            src_ip=self.local_info.ip,
            dst_ip=subnet.split("/")[0],
            opcode=1,
        )

        # srp is blocking; run it in a thread to avoid freezing the loop
        answered, _ = await asyncio.to_thread(srp, arp_pkt, timeout=2, verbose=False)
        return [{"ip": rcvd.psrc, "mac": rcvd.hwsrc} for _, rcvd in answered]

    async def icmp_ping_sweep(self, ip_range: Iterable[str], timeout: int = 1) -> List[str]:
        async def ping(ip: str) -> Optional[str]:
            pkt = self.crafter.craft_icmp_echo(ip)
            # sr1 is blocking; run in a thread
            resp = await asyncio.to_thread(sr1, pkt, timeout=timeout, verbose=False)
            return ip if resp else None

        tasks = [asyncio.create_task(ping(ip)) for ip in ip_range]
        results = await asyncio.gather(*tasks)
        return [ip for ip in results if ip]

    async def tcp_port_scan(self, target: str, ports: Iterable[int], timeout: float = 1.0) -> Dict[int, str]:
        def scan_one(port: int) -> Optional[int]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                result = sock.connect_ex((target, port))
                return port if result == 0 else None
            finally:
                sock.close()

        tasks = [asyncio.to_thread(scan_one, p) for p in ports]
        results = await asyncio.gather(*tasks)
        return {p: "open" for p in results if p is not None}
