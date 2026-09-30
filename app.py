
from flask import Flask, render_template
import socket
import platform
import re
from pathlib import Path

app = Flask(__name__)


# 1. System Information
def get_system_info():

    hostname = socket.gethostname()

    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip = "Unavailable"

    os_name = platform.system()

    return hostname, ip, os_name


# 2. Network Port Monitoring
def check_ports():

    ports = {
        22: "SSH",
        53: "DNS",
        80: "HTTP",
        443: "HTTPS"
    }

    results = {}

    for port, service in ports.items():

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(1)

        try:
            result = sock.connect_ex(
                ("127.0.0.1", port)
            )

            status = "OPEN" if result == 0 else "CLOSED"

        except OSError:
            status = "ERROR"

        finally:
            sock.close()

        results[port] = {
            "service": service,
            "status": status
        }

    return results


# 3. DNS Resolution
def check_dns():

    try:
        return socket.gethostbyname("google.com")

    except socket.gaierror:
        return "Resolution Failed"


# 4. Authentication Log Analysis
def analyze_logs():

    log_file = Path("auth.log")

    if not log_file.exists():
        return 0

    try:
        content = log_file.read_text(
            errors="ignore"
        )

        pattern = r"Failed password"

        return len(
            re.findall(pattern, content)
        )

    except OSError:
        return 0


# 5. Dashboard Route
@app.route("/")
def dashboard():

    hostname, ip, os_name = get_system_info()

    ports = check_ports()

    dns = check_dns()

    failed_count = analyze_logs()

    critical = 1 if failed_count >= 5 else 0

    total_events = failed_count 

    return render_template(
        "dashboard.html",
        hostname=hostname,
        ip=ip,
        os_name=os_name,
        dns=dns,
        ports=ports,
        failed_count=failed_count,
        critical=critical,
        total_events=total_events
    )


# 6. Start Flask Server
# 6. Security Alerts Page
@app.route("/alerts")
def alerts_page():

    log_file = Path("auth.log")

    alerts = []

    if log_file.exists():

        try:
            content = log_file.read_text(errors="ignore")

            for line in content.splitlines():

                if "Failed password" in line:
                    alerts.append(line)

        except OSError:
            alerts = []

    return render_template(
        "alerts.html",
        alerts=alerts,
        failed_count=len(alerts)
    )

# 7. Start Flask Server
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
