import socket
import ipaddress
import uuid

hostname = socket.gethostname()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()

ip = ipaddress.ip_address(ip_address)

if ip.is_private:
    ip_type = "Private IP"
else:
    ip_type = "Public IP"

mac = uuid.getnode()

mac_address = ':'.join(
    f'{(mac >> i) & 0xff:02x}'
    for i in range(40, -1, -8)
)

print("================================")
print(" SOC BASIC SECURITY MONITOR")
print("================================")

print("Hostname  :", hostname)
print("IP Address:", ip_address)
print("IP Type   :", ip_type)
print("MAC Address:", mac_address)
common_ports = {
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS"
}

print()
print("Common Port Information")
print("-----------------------")

for port, service in common_ports.items():
    print(f"Port {port} : {service}")
print()
print("TCP Port Check")
print("--------------")

target = "127.0.0.1"

for port, service in common_ports.items():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex((target, port))

    if result == 0:
        status = "OPEN"
    else:
        status = "CLOSED"

    sock.close()

    print(f"Port {port} ({service}) : {status}")
print()
print("DNS Resolution Check")
print("--------------------")

domain = "google.com"

try:
    dns_ip = socket.gethostbyname(domain)
    print("Domain :", domain)
    print("IP     :", dns_ip)
    print("Status : DNS Resolution Successful")

except socket.gaierror:
    print("Domain :", domain)
    print("Status : DNS Resolution Failed")
print()
print("Authentication Log Analysis")
print("---------------------------")

failed_count = 0

with open("auth.log", "r") as file:
    for line in file:
        if "Failed password" in line:
            failed_count += 1

print("Failed Login Attempts:", failed_count)
