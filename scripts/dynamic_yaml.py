#!/usr/bin/env python3
import re

LEASE_FILE = "/var/lib/dhcpd/dhcpd.leases"

def parse_leases(file_path):
    leases = {}
    with open(file_path, 'r') as file:
        current_lease = None
        for line in file:
            if line.startswith("lease "):
                ip_address = line.split()[1]
                current_lease = {"ip": ip_address}
            elif line.strip() == "}":
                leases[current_lease["ip"]] = current_lease
                current_lease = None
            elif current_lease is not None:
                if "client-hostname" in line:
                    current_lease["hostname"] = re.search(r'"(.*?)"', line).group(1)

    return list(leases.values())

def main():
    leases = parse_leases(LEASE_FILE)
    
    print("[leerlingen]")
    for lease in leases:
        hostname = lease.get("hostname", "PC{}".format(lease["ip"].split('.')[-1]))
        print("{} ansible_host={}".format(hostname, lease["ip"]))
    
    print("\n[leerlingen:vars]")
    print("ansible_ssh_private_key_file=~/.ssh/test")
    print("ansible_user=root")
    print("ansible_host_key_checking=False")

if __name__ == "__main__":
    main()
