import subprocess
# Drew Laikin
# Script to set up security measures for Ubuntu servers

# subprocess parser
def run_cmd(cmd):
    subprocess.run(cmd.split())


# fail2ban
run_cmd("sudo apt -y install fail2ban")
run_cmd("sudo cp /etc/fail2ban/fail2ban.conf /etc/fail2ban/fail2ban.local")
run_cmd("sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local")
file = open("/etc/fail2ban/jail.local", "r+")
lines = file.readlines()
for each in lines:
    if "maxretry" in each and "#" not in each:
        lines[lines.index(each)] = "maxretry = 2\n"
        break

file.seek(0)
file.writelines(lines)
file.close()
run_cmd("sudo systemctl restart fail2ban")

# Firewall Setup
run_cmd("sudo systemctl disable iptables")
run_cmd("sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT")
run_cmd("sudo iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT")
run_cmd("sudo iptables -A INPUT -i lo -j ACCEPT")
run_cmd("sudo iptables -A INPUT -p tcp --dport 9418 -j ACCEPT")
run_cmd("sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT")
run_cmd("sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT")
run_cmd("sudo iptables -A INPUT -j DROP")
run_cmd("sudo systemctl enable iptables")
