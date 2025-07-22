import json
import csv
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

class ReportBuilder:
    def __init__(self, scan_data):
        self.data = scan_data
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Set up template environment
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.filters['datetimeformat'] = self._format_datetime
        
    def _format_datetime(self, timestamp):
        """Jinja2 filter to format timestamp"""
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp
    
    def _prepare_network_data(self):
        """Format network scan data for reporting"""
        if 'network' not in self.data and 'devices' not in self.data:
            return None
            
        devices = self.data.get('network') or self.data.get('devices') or {}
        formatted = []
        
        for mac, info in devices.items():
            formatted.append({
                'ip': info.get('ip', 'N/A'),
                'mac': mac,
                'vendor': info.get('vendor', 'Unknown'),
                'first_seen': info.get('first_seen'),
                'last_seen': info.get('last_seen', info.get('last_seen')),
                'duration': info.get('duration', 0)
            })
        return sorted(formatted, key=lambda x: x['ip'])
    
    def _prepare_web_data(self):
        """Format web scan data for reporting"""
        web_data = self.data.get('web') or {}
        formatted = []
        
        for url, results in web_data.items():
            entry = {'url': url}
            
            # Subdomains
            if 'subdomains' in results:
                entry['subdomains'] = results['subdomains']
            
            # Paths
            if 'paths' in results:
                entry['paths'] = [{'url': p[0], 'status': p[1]} for p in results['paths']]
            
            # Technologies
            if 'tech' in results:
                tech = results['tech']
                if isinstance(tech, dict):
                    entry['technologies'] = tech
                elif isinstance(tech, list):
                    entry['technologies'] = {'detected': tech}
            
            formatted.append(entry)
        return formatted
    
    def to_txt(self, filename=None):
        """Generate text report"""
        filename = filename or f"{self.report_id}.txt"
        
        output = [
            f"GhostEyes Security Report",
            f"Generated: {self.timestamp}",
            f"{'=' * 50}\n"
        ]
        
        # Network section
        network_data = self._prepare_network_data()
        if network_data:
            output.append("[NETWORK DEVICES]")
            output.append(f"{'IP Address':<15} {'MAC Address':<18} {'Vendor':<25} {'First Seen':<20} {'Duration (s)':>12}")
            output.append("-" * 85)
            
            for device in network_data:
                first_seen = self._format_datetime(device['first_seen']) if device.get('first_seen') else 'N/A'
                output.append(
                    f"{device['ip']:<15} {device['mac']:<18} {device['vendor'][:24]:<25} "
                    f"{first_seen:<20} {device.get('duration', 0):>12.1f}"
                )
            output.append("")
        
        # Web section
        web_data = self._prepare_web_data()
        if web_data:
            output.append("[WEB RECONNAISSANCE]")
            for site in web_data:
                output.append(f"\nURL: {site['url']}")
                
                # Subdomains
                if 'subdomains' in site:
                    output.append(f"\n  Subdomains ({len(site['subdomains'])}):")
                    for sub in site['subdomains']:
                        output.append(f"    - {sub}")
                
                # Paths
                if 'paths' in site:
                    output.append(f"\n  Accessible Paths ({len(site['paths'])}):")
                    for path in site['paths']:
                        output.append(f"    - {path['url']} (HTTP {path['status']})")
                
                # Technologies
                if 'technologies' in site:
                    output.append("\n  Technologies:")
                    for category, items in site['technologies'].items():
                        if isinstance(items, list):
                            output.append(f"    {category.title()}: {', '.join(items)}")
                        elif isinstance(items, dict):
                            for key, value in items.items():
                                output.append(f"    {key}: {value}")
            output.append("")
        
        # Write to file
        with open(filename, 'w') as f:
            f.write("\n".join(output))
        return filename
    
    def to_json(self, filename=None):
        """Generate JSON report"""
        filename = filename or f"{self.report_id}.json"
        
        report = {
            'metadata': {
                'tool': 'GhostEyes',
                'version': '2.0',
                'generated': self.timestamp,
                'report_id': self.report_id
            },
            'data': self.data
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        return filename
    
    def to_html(self, filename=None):
        """Generate HTML report"""
        filename = filename or f"{self.report_id}.html"
        
        template = self.env.get_template('report_template.html')
        
        html_output = template.render(
            report_id=self.report_id,
            generated=self.timestamp,
            network_data=self._prepare_network_data(),
            web_data=self._prepare_web_data(),
            vlans=self.data.get('vlans'),
            trace=self.data.get('trace'),
            dhcp=self.data.get('dhcp')
        )
        
        with open(filename, 'w') as f:
            f.write(html_output)
        return filename
    
    def to_csv(self, filename=None):
        """Generate CSV report"""
        filename = filename or f"{self.report_id}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Type', 'IP', 'MAC', 'Vendor', 'First Seen', 'Last Seen', 'Duration', 'Details'])
            
            # Network devices
            network_data = self._prepare_network_data()
            if network_data:
                for device in network_data:
                    first_seen = self._format_datetime(device['first_seen']) if device.get('first_seen') else ''
                    last_seen = self._format_datetime(device['last_seen']) if device.get('last_seen') else ''
                    writer.writerow([
                        'device',
                        device['ip'],
                        device['mac'],
                        device['vendor'],
                        first_seen,
                        last_seen,
                        device.get('duration', ''),
                        ''
                    ])
            
            # Web technologies
            web_data = self._prepare_web_data()
            if web_data:
                for site in web_data:
                    # Subdomains
                    if 'subdomains' in site:
                        for sub in site['subdomains']:
                            writer.writerow([
                                'subdomain',
                                '',
                                '',
                                '',
                                '',
                                '',
                                '',
                                f"{sub} (parent: {site['url']})"
                            ])
                    
                    # Paths
                    if 'paths' in site:
                        for path in site['paths']:
                            writer.writerow([
                                'path',
                                '',
                                '',
                                '',
                                '',
                                '',
                                '',
                                f"{path['url']} | Status: {path['status']}"
                            ])
                    
                    # Technologies
                    if 'technologies' in site:
                        for category, items in site['technologies'].items():
                            if isinstance(items, list):
                                writer.writerow([
                                    'technology',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    f"{category}: {', '.join(items)}"
                                ])
                            elif isinstance(items, dict):
                                for key, value in items.items():
                                    writer.writerow([
                                        'technology',
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        f"{key}: {value}"
                                    ])
        return filename
