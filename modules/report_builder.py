import json
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>GhostEyes Report</title></head>
<body>
<h1>Scan Results</h1>
{% for section in sections %}
<div class="section">
  <h2>{{ section.title }}</h2>
  <pre>{{ section.content }}</pre>
</div>
{% endfor %}
</body>
</html>
"""

class ReportBuilder:
    def __init__(self, scan_data):
        self.data = scan_data
        
    def to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
            
    def to_html(self, filename):
        sections = [
            {"title": "Network Hosts", "content": "\n".join(
                [f"{host['ip']} ({host['mac']})" for host in self.data['hosts']])},
            {"title": "Web Technologies", "content": ", ".join(
                self.data['tech_stack'])}
        ]
        template = Template(HTML_TEMPLATE)
        with open(filename, 'w') as f:
            f.write(template.render(sections=sections))
