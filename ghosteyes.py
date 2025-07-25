#!/usr/bin/env python3
# © Copyright 6lackRaven 2025
# License MIT



import asyncio
import argparse
import json
import sys
from textwrap import dedent

from modules import (
    vlan_explorer,
    web_scanner,
    device_tracker,
    reporter,
    l2_traceroute,
    dhcp_snooper,
)
from core.scanner import NetworkScanner
from core.utils import get_interface_details, validate_cidr

# ---- Colors ----
CRED = "\033[91m"
CGREEN = "\033[92m"
CYELLOW = "\033[93m"
CBLUE = "\033[94m"
CEND = "\033[0m"

VERSION = "v2.1.0"
AUTHOR = "6lackRaven"


def banner():
    print(dedent(f"""
    {CBLUE}========================================={CEND}
    {CGREEN}   GhostEyes {VERSION} - Offensive Recon Toolkit{CEND}
    {CYELLOW}   Author: {AUTHOR}{CEND}
    {CBLUE}========================================={CEND}
    """))


def build_parser() -> argparse.ArgumentParser:
    description = dedent(f"""\
        {CGREEN}GhostEyes {VERSION} - Offensive Reconnaissance Toolkit{CEND}
        ------------------------------------------------
        Commands:
          net     Network reconnaissance (ARP, VLANs, devices, traceroute, DHCP)
          web     Web reconnaissance (subdomains, dirs, tech stack)
          report  Generate reports from previous scans
    """)

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--version", action="store_true", help="Show version info and exit")
    parser.add_argument("--examples", action="store_true", help="Show usage examples")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose logs")

    subparsers = parser.add_subparsers(dest="command", required=False)

    # ---- net ----
    net_parser = subparsers.add_parser("net", help="Network reconnaissance")
    net_parser.add_argument("-i", "--interface", default="eth0", help="Network interface")
    net_group = net_parser.add_mutually_exclusive_group(required=True)
    net_group.add_argument("-s", "--scan", metavar="CIDR", help="Scan subnet (e.g., 192.168.1.0/24)")
    net_group.add_argument("-v", "--vlan", action="store_true", help="Discover VLANs")
    net_group.add_argument("-t", "--track", action="store_true", help="Track live devices")
    net_group.add_argument("-r", "--trace", metavar="IP", help="Layer 2 traceroute to target")
    net_group.add_argument("-d", "--dhcp", action="store_true", help="Capture DHCP traffic")
    net_parser.add_argument("--duration", type=int, default=300, help="Operation duration (seconds)")
    net_parser.add_argument("--output", default="scan_net.json", help="Output JSON file")

    # ---- web ----
    web_parser = subparsers.add_parser("web", help="Web reconnaissance")
    web_parser.add_argument("-u", "--url", required=True, help="Target URL")
    web_parser.add_argument("-s", "--subdomains", metavar="WORDLIST", help="Subdomain brute-force wordlist")
    web_parser.add_argument("-b", "--bruteforce", metavar="WORDLIST", help="Directory brute-force wordlist")
    web_parser.add_argument("-T", "--tech", action="store_true", help="Detect technologies")
    web_parser.add_argument("-w", "--workers", type=int, default=50, help="Concurrent workers")
    web_parser.add_argument("--output", default="scan_web.json", help="Output JSON file")

    # ---- report ----
    report_parser = subparsers.add_parser("report", help="Generate reports")
    report_parser.add_argument("-f", "--file", required=True, help="Scan results file (JSON)")
    report_parser.add_argument(
        "-t", "--type", choices=["txt", "json", "html", "csv", "all"],
        default=["html"], nargs="+", help="Output formats"
    )

    return parser


def show_examples():
    print(dedent(f"""
        {CYELLOW}Usage Examples:{CEND}
        {CBLUE}# Network ARP scan{CEND}
        python ghosteyes.py net -i eth0 --scan 192.168.1.0/24

        {CBLUE}# VLAN discovery for 2 minutes{CEND}
        python ghosteyes.py net -i eth0 --vlan --duration 120

        {CBLUE}# Track devices{CEND}
        python ghosteyes.py net -i wlan0 --track --duration 60

        {CBLUE}# Web scan with subdomains + tech detection{CEND}
        python ghosteyes.py web -u https://example.com -s subdomains.txt -T

        {CBLUE}# Generate HTML and JSON reports{CEND}
        python ghosteyes.py report -f scan_net.json -t html json
    """))


async def handle_net(args, quiet=False) -> dict:
    scan_data = {}
    iface_info = await get_interface_details(args.interface)
    if not quiet:
        print(f"{CYELLOW}Using interface:{CEND} {iface_info.name} ({iface_info.ip})")

    if args.scan:
        if not validate_cidr(args.scan):
            print(f"{CRED}Invalid CIDR format:{CEND} {args.scan}")
            return scan_data

        if not quiet:
            print(f"{CBLUE}Scanning subnet:{CEND} {args.scan}")
        scanner = NetworkScanner(args.interface, iface_info)
        hosts = await scanner.arp_scan(args.scan)
        scan_data["network"] = {host["ip"]: host for host in hosts}
        print(f"{CGREEN}Found {len(hosts)} active hosts{CEND}")

    elif args.vlan:
        if not quiet:
            print(f"{CBLUE}Starting VLAN discovery...{CEND}")
        vlan_scanner = vlan_explorer.VLANExplorer(args.interface)
        vlans = await vlan_scanner.sniff_vlans(duration=args.duration)
        print(f"{CGREEN}Discovered VLANs:{CEND} {', '.join(map(str, vlans)) or 'None'}")

        if vlans:
            scan_data["vlans"] = {}
            for vlan in list(vlans)[:3]:
                if not quiet:
                    print(f"{CBLUE}Scanning VLAN {vlan}...{CEND}")
                result = await vlan_scanner.discover_vlan_devices(vlan)
                scan_data["vlans"][vlan] = list(result.devices)

    elif args.track:
        if not quiet:
            print(f"{CBLUE}Tracking devices for {args.duration} seconds...{CEND}")
        tracker = device_tracker.DeviceTracker(interface=args.interface, refresh_interval=10)
        devices = await tracker.start_monitoring(duration=args.duration)
        scan_data["devices"] = devices
        print(f"{CGREEN}Tracked {len(devices)} devices{CEND}")

    elif args.trace:
        if not quiet:
            print(f"{CBLUE}Tracing path to {args.trace}...{CEND}")
        tracer = l2_traceroute.Layer2Traceroute(args.interface)
        path = await tracer.trace(args.trace)
        scan_data["trace"] = [hop._asdict() for hop in path]
        for i, hop in enumerate(path):
            print(f"Hop {i+1}: {hop.ip} ({hop.mac}) - {hop.vendor}")

    elif args.dhcp:
        if not quiet:
            print(f"{CBLUE}Capturing DHCP traffic for {args.duration} seconds...{CEND}")
        snooper = dhcp_snooper.DHCPSnooper(args.interface)
        await snooper.capture_dhcp(duration=args.duration)
        scan_data["dhcp"] = snooper.leases
        print(f"{CGREEN}Captured {len(snooper.leases)} DHCP transactions{CEND}")

    return scan_data


async def handle_web(args, quiet=False) -> dict:
    scan_data = {}
    if not quiet:
        print(f"{CBLUE}Starting web reconnaissance on {args.url}{CEND}")

    async with web_scanner.WebScanner() as scanner:
        results = {}

        if args.subdomains:
            if not quiet:
                print(f"{CYELLOW}Enumerating subdomains...{CEND}")
            with open(args.subdomains) as f:
                wordlist = [line.strip() for line in f if line.strip()]
            domain = web_scanner.extract_domain(args.url)
            subdomains = await scanner.subdomain_scan(domain, wordlist, workers=args.workers)
            results["subdomains"] = subdomains
            print(f"{CGREEN}Found {len(subdomains)} valid subdomains{CEND}")

        if args.bruteforce:
            if not quiet:
                print(f"{CYELLOW}Brute-forcing directories...{CEND}")
            with open(args.bruteforce) as f:
                wordlist = [line.strip() for line in f if line.strip()]
            paths = await scanner.dir_bruteforce(args.url, wordlist, workers=args.workers)
            results["paths"] = paths
            print(f"{CGREEN}Found {len(paths)} accessible paths{CEND}")

        if args.tech:
            if not quiet:
                print(f"{CYELLOW}Detecting technologies...{CEND}")
            tech = await scanner.tech_detect(args.url)
            results["tech"] = tech
            print(f"{CGREEN}Technology stack identified{CEND}")

        scan_data["web"] = {args.url: results}

    return scan_data


def handle_report(args):
    print(f"{CBLUE}Generating report from {args.file}{CEND}")
    try:
        with open(args.file) as f:
            scan_data = json.load(f)
    except FileNotFoundError:
        print(f"{CRED}File not found:{CEND} {args.file}")
        return
    except json.JSONDecodeError:
        print(f"{CRED}Invalid JSON format in {args.file}{CEND}")
        return

    rb = reporter.ReportBuilder(scan_data)
    formats = args.type
    if "all" in formats:
        formats = ["txt", "json", "html", "csv"]

    output_files = []
    for fmt in formats:
        if fmt == "txt":
            output_files.append(rb.to_txt())
        elif fmt == "json":
            output_files.append(rb.to_json())
        elif fmt == "html":
            output_files.append(rb.to_html())
        elif fmt == "csv":
            output_files.append(rb.to_csv())

    print(f"{CGREEN}Generated reports:{CEND} {', '.join(output_files)}")


async def async_main(args):
    try:
        quiet = args.quiet
        if args.command == "net":
            scan_data = await handle_net(args, quiet)
        elif args.command == "web":
            scan_data = await handle_web(args, quiet)
        elif args.command == "report":
            handle_report(args)
            return
        else:
            print(f"{CRED}Unknown command. Use -h for help.{CEND}")
            return

        if args.command != "report" and scan_data:
            filename = args.output
            with open(filename, "w") as f:
                json.dump(scan_data, f, indent=2)
            print(f"{CYELLOW}Scan results saved to {filename}{CEND}")

    except PermissionError:
        print(f"{CRED}Permission denied - try running with sudo{CEND}")
    except KeyboardInterrupt:
        print(f"{CYELLOW}\nOperation cancelled by user{CEND}")
    except Exception as e:
        print(f"{CRED}Critical error:{CEND} {str(e)}")
        sys.exit(1)


def main():
    banner()
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"GhostEyes {VERSION} by {AUTHOR}")
        return

    if args.examples:
        show_examples()
        return

    if not args.command:
        parser.print_help()
        return

    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
