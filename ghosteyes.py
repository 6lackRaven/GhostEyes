#!/usr/bin/env python3

# GhostEyes - A powerful network recon tool
# Copyright (c) 2025 6lackRaven
# Licensed under the MIT License


import asyncio
import argparse
import json
import sys
from modules import (
    vlan_explorer, 
    web_scanner, 
    device_tracker, 
    reporter,
    l2_traceroute,
    dhcp_snooper
)
from core.scanner import NetworkScanner
from core.utils import get_interface_details, validate_cidr

async def main():
    parser = argparse.ArgumentParser(
        description="GhostEyes v2 - Offensive Reconnaissance Toolkit",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Network reconnaissance
    net_parser = subparsers.add_parser('net', help='Network reconnaissance')
    net_parser.add_argument('-i', '--interface', default='eth0', help='Network interface')
    net_group = net_parser.add_mutually_exclusive_group(required=True)
    net_group.add_argument('-s', '--scan', metavar='CIDR', help='Scan subnet (e.g., 192.168.1.0/24)')
    net_group.add_argument('-v', '--vlan', action='store_true', help='Discover VLANs')
    net_group.add_argument('-t', '--track', action='store_true', help='Track live devices')
    net_group.add_argument('-r', '--trace', metavar='IP', help='Layer 2 traceroute to target')
    net_group.add_argument('-d', '--dhcp', action='store_true', help='Capture DHCP traffic')
    net_parser.add_argument('--duration', type=int, default=300, help='Operation duration (seconds)')
    
    # Web reconnaissance
    web_parser = subparsers.add_parser('web', help='Web reconnaissance')
    web_parser.add_argument('-u', '--url', required=True, help='Target URL')
    web_parser.add_argument('-s', '--subdomains', metavar='WORDLIST', help='Subdomain brute-force wordlist')
    web_parser.add_argument('-b', '--bruteforce', metavar='WORDLIST', help='Directory brute-force wordlist')
    web_parser.add_argument('-T', '--tech', action='store_true', help='Detect technologies')
    web_parser.add_argument('-w', '--workers', type=int, default=50, help='Concurrent workers')
    
    # Reporting
    report_parser = subparsers.add_parser('report', help='Generate reports')
    report_parser.add_argument('-f', '--file', required=True, help='Scan results file (JSON)')
    report_parser.add_argument('-t', '--type', choices=['txt', 'json', 'html', 'csv', 'all'], 
                              default=['html'], nargs='+', help='Output formats')
    
    args = parser.parse_args()
    scan_data = {}
    
    try:
        # Validate interface for network commands
        if args.command == 'net':
            iface_info = await get_interface_details(args.interface)
            print(f"ℹ️ Using interface: {iface_info.name} ({iface_info.ip})")
            
            # Subnet scanning
            if args.scan:
                if not validate_cidr(args.scan):
                    print(f"❌ Invalid CIDR format: {args.scan}")
                    return
                
                print(f"🔍 Scanning subnet: {args.scan}")
                scanner = NetworkScanner(args.interface)
                hosts = await scanner.arp_scan(args.scan)
                scan_data['network'] = {host['ip']: host for host in hosts}
                print(f"✅ Found {len(hosts)} active hosts")
            
            # VLAN discovery
            elif args.vlan:
                print("🌐 Starting VLAN discovery...")
                vlan_scanner = vlan_explorer.VLANExplorer(args.interface)
                vlans = await vlan_scanner.sniff_vlans(duration=args.duration)
                print(f"✅ Discovered VLANs: {', '.join(map(str, vlans)) or 'None'}")
                
                if vlans:
                    scan_data['vlans'] = {}
                    for vlan in list(vlans)[:3]:  # Limit to first 3
                        print(f"🔍 Scanning VLAN {vlan}...")
                        result = await vlan_scanner.discover_vlan_devices(vlan)
                        scan_data['vlans'][vlan] = list(result.devices)
                        print(f"  → Found {len(result.devices)} devices")
            
            # Device tracking
            elif args.track:
                print(f"👀 Tracking devices for {args.duration} seconds...")
                tracker = device_tracker.DeviceTracker(
                    interface=args.interface,
                    refresh_interval=10
                )
                devices = await tracker.start_monitoring(duration=args.duration)
                scan_data['devices'] = devices
                print(f"✅ Tracked {len(devices)} devices")
            
            # Layer 2 traceroute
            elif args.trace:
                print(f"🕵️ Tracing path to {args.trace}...")
                tracer = l2_traceroute.Layer2Traceroute(args.interface)
                path = await tracer.trace(args.trace)
                scan_data['trace'] = [hop._asdict() for hop in path]
                for i, hop in enumerate(path):
                    print(f"Hop {i+1}: {hop.ip} ({hop.mac}) - {hop.vendor}")
            
            # DHCP snooping
            elif args.dhcp:
                print(f"📡 Capturing DHCP traffic for {args.duration} seconds...")
                snooper = dhcp_snooper.DHCPSnooper(args.interface)
                await snooper.capture_dhcp(duration=args.duration)
                scan_data['dhcp'] = snooper.leases
                print(f"✅ Captured {len(snooper.leases)} DHCP transactions")
        
        # Web reconnaissance
        elif args.command == 'web':
            print(f"🌐 Starting web reconnaissance on {args.url}")
            async with web_scanner.WebScanner() as scanner:
                results = {}
                
                # Subdomain enumeration
                if args.subdomains:
                    print(f"🔎 Enumerating subdomains...")
                    with open(args.subdomains) as f:
                        wordlist = [line.strip() for line in f if line.strip()]
                    domain = web_scanner.extract_domain(args.url)
                    subdomains = await scanner.subdomain_scan(
                        domain, wordlist, workers=args.workers
                    )
                    results['subdomains'] = subdomains
                    print(f"✅ Found {len(subdomains)} valid subdomains")
                
                # Directory brute-forcing
                if args.bruteforce:
                    print(f"🚪 Brute-forcing directories...")
                    with open(args.bruteforce) as f:
                        wordlist = [line.strip() for line in f if line.strip()]
                    paths = await scanner.dir_bruteforce(
                        args.url, wordlist, workers=args.workers
                    )
                    results['paths'] = paths
                    print(f"✅ Found {len(paths)} accessible paths")
                
                # Technology detection
                if args.tech:
                    print(f"🔧 Detecting technologies...")
                    tech = await scanner.tech_detect(args.url)
                    results['tech'] = tech
                    print("✅ Technology stack identified")
                
                scan_data['web'] = {args.url: results}
        
        # Reporting
        elif args.command == 'report':
            print(f"📊 Generating report from {args.file}")
            try:
                with open(args.file) as f:
                    scan_data = json.load(f)
            except FileNotFoundError:
                print(f"❌ File not found: {args.file}")
                return
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON format in {args.file}")
                return
            
            report = reporter.ReportBuilder(scan_data)
            formats = args.type
            if 'all' in formats:
                formats = ['txt', 'json', 'html', 'csv']
            
            output_files = []
            for fmt in formats:
                if fmt == 'txt':
                    output_files.append(report.to_txt())
                elif fmt == 'json':
                    output_files.append(report.to_json())
                elif fmt == 'html':
                    output_files.append(report.to_html())
                elif fmt == 'csv':
                    output_files.append(report.to_csv())
            
            print(f"✅ Generated reports: {', '.join(output_files)}")
        
        # Save scan results if not reporting
        if args.command != 'report' and scan_data:
            filename = f"scan_{args.command}.json"
            with open(filename, 'w') as f:
                json.dump(scan_data, f, indent=2)
            print(f"💾 Scan results saved to {filename}")
    
    except PermissionError:
        print("❌ Permission denied - try running with sudo")
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
