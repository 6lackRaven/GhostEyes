import json
import csv
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

class ReportBuilder:
    def __init__(self, scan_data):
        self.data = scan_data
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def to_txt(self, filename=None):
        """Generate text report"""
        filename = filename or f"report_{self.timestamp}.txt"
        output = []
        
        # Network section
        if 'network' in self.data:
            output.append("[Network Devices]")
            for device in self.data['network'].values():
                output.append(f"{device['ip']} ({device['mac']}) - {device.get('vendor', 'Unknown')}")
        
        # Web section
        if 'web' in self.data:
            output.append("\n[Web Technologies]")
            for url, tech in self.data['web'].items():
                output.append(f"\n{url}:")
                for category, items in tech.items():
                    output.append(f"  {category.title()}: {', '.join(items)}")
        
        with open(filename, 'w') as f:
            f.write("\n".join(output))
        return filename
    
    def to_json(self, filename=None):
        """Generate JSON report"""
        filename = filename or f"report_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        return filename
    
    def to_html(self, filename=None):
        """Generate HTML report"""
        filename = filename or f"report_{self.timestamp}.html"
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('report_template.html')
        
        html_output = template.render(
            scan_data=self.data,
            timestamp=self.timestamp
        )
        
        with open(filename, 'w') as f:
            f.write(html_output)
        return filename
    
    def to_csv(self, filename=None):
        """Generate CSV report"""
        filename = filename or f"report_{self.timestamp}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Type', 'IP', 'MAC', 'Vendor', 'First Seen', 'Duration'])
            
            # Write network data
            if 'network' in self.data:
                for device in self.data['network'].values():
                    writer.writerow([
                        'device',
                        device.get('ip', '
