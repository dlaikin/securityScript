import subprocess
# Drew Laikin
# Script to set up security measures for Ubuntu servers

# fail2ban
subprocess.run(["sudo", "apt", "-y", "install", "fail2ban"])
subprocess.run(["sudo", "cp", "/etc/fail2ban/fail2ban.conf", "/etc/fail2ban/fail2ban.local"])
subprocess.run(["sudo", "cp", "/etc/fail2ban/jail.conf", "/etc/fail2ban/jail.local"])
file = open("/etc/fail2ban/jail.local", "r+")
lines = file.readlines()
for each in lines:
    if "maxretry" in each and "#" not in each:
        lines.insert(lines.index(each), "maxretry = 2\n")
        break
file.seek(0)
file.writelines(lines)
file.close()
subprocess.run(["sudo", "systemctl", "restart", "fail2ban"])

# Firewall Setup
subprocess.run(["sudo", "systemctl","disable", "iptables"])
subprocess.run(["sudo", "iptables", "-A" , "INPUT", "-j", "DROP"])
subprocess.run(["sudo", "iptables", "-A" , "INPUT", "-m", "conntrack", "--ctstate", "RELATED,ESTABLISHED", "-j", "ACCEPT"])
subprocess.run(["sudo", "iptables", "-A" , "INPUT", "-i", "lo", "-j", "ACCEPT"])
subprocess.run(["sudo", "iptables", "-I" , "INPUT", "-p", "tcp", "--dport", "22", "-j", "ACCEPT"])
subprocess.run(["sudo", "iptables", "-A" , "INPUT", "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
subprocess.run(["sudo", "iptables", "-A" , "INPUT", "-p", "tcp", "--dport", "80", "-j", "ACCEPT"])
subprocess.run(["sudo", "systemctl","enable", "iptables"])