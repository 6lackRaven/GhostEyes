from flask import Flask, render_template_string, request
import socket
import threading
import time
from queue import Queue
from datetime import datetime

import platform
from ghosteyes import portscan, worker, fill_queue, os_detection, tech_fingerprint, common_services

app = Flask(__name__)

common_services = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 8080: "HTTP-ALT",
}

HTML_FORM = '''
<!doctype html>
<title>GhostEyes Port Scanner</title>
<h2>GhostEyes - Port Scanner Tool</h2>
<form method=post>
  Target IP/Domain: <input name=target required value="{{ request.form.target if request.form.get('target') else '' }}"><br>
  Start Port: <input name=start type=number value="{{ request.form.start if request.form.get('start') else 1 }}"><br>
  End Port: <input name=end type=number value="{{ request.form.end if request.form.get('end') else 1024 }}"><br>
  Threads: <input name=threads type=number value="{{ request.form.threads if request.form.get('threads') else 50 }}"><br>
  Detect OS/Web: <input name=detect type=checkbox {% if request.form.get('detect') %}checked{% endif %}><br>
  <input type=submit value=Scan>
</form>
{% if error %}
  <div style="color:red"><b>{{ error }}</b></div>
{% endif %}
{% if result %}
  <h3>Scan Results</h3>
  <div>{{ result|safe }}</div>
{% endif %}
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        target = request.form['target'].strip()
        start = request.form.get('start', '1').strip()
        end = request.form.get('end', '1024').strip()
        threads_count = request.form.get('threads', '50').strip()
        mode = 'basic'
        detect = 'detect' in request.form
        output_file = request.form.get('output', '').strip()
        # Inputvalidering
        try:
            start = int(start)
            end = int(end)
            threads_count = int(threads_count)
            if start < 1 or end > 65535 or start > end:
                raise ValueError
        except ValueError:
            error = "Felaktigt portintervall. Ange giltiga heltal mellan 1 och 65535."
            return render_template_string(HTML_FORM, result=None, error=error, request=request)
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            error = "Fel: Kunde inte slå upp mål (target)."
            return render_template_string(HTML_FORM, result=None, error=error, request=request)
        # Använd ghosteyes.py:s globala queue och open_ports
        from ghosteyes import queue as ghost_queue, open_ports as ghost_open_ports
        # Töm queue och open_ports innan ny scanning
        while not ghost_queue.empty():
            ghost_queue.get()
        ghost_open_ports.clear()
        fill_queue(start, end)
        threads = []
        t0 = time.time()
        for _ in range(threads_count):
            t = threading.Thread(target=worker, args=(target_ip, mode))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        duration = time.time() - t0
        # Systeminfo
        try:
            hostname = socket.gethostbyaddr(target_ip)[0]
        except:
            hostname = "Unknown"
        sysinfo = f"Target IP   : {target_ip}\nHostname    : {hostname}\nYour OS     : {platform.system()} {platform.release()}\nStart Time  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'-'*40}\n"
        # Tabell för öppna portar
        output = sysinfo
        output += "<b>Open Ports:</b><br>"
        if ghost_open_ports:
            output += "<table border=1 cellpadding=3><tr><th>Port</th><th>Status</th><th>Service/Banner</th></tr>"
            for port, service in sorted(ghost_open_ports):
                output += f"<tr><td>{port}</td><td style='color:green'>Open</td><td>{service}</td></tr>"
            output += "</table>"
        else:
            output += "Inga öppna portar hittades.<br>"
        output += f"<br>Duration: {duration:.2f} seconds<br>"
        if detect:
            output += f"<br><b>OS Detection:</b> {os_detection(target_ip)}<br>"
            output += f"<b>Web Tech:</b> {tech_fingerprint(target_ip)}<br>"
        # Spara till fil om önskat
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(output)
                output += f"\nResultat sparat i {output_file}"
            except Exception as e:
                output += f"\nKunde inte spara till fil: {e}"
        result = output
    return render_template_string(HTML_FORM, result=result, error=error, request=request)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
