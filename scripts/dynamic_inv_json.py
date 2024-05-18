#!/usr/bin/env python3
import re
import json

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

def generate_inventory_json():
    leases = parse_leases(LEASE_FILE)

    inventory = {
        "_meta": {
            "hostvars": {}
        },
        "leerlingen": {
            "hosts": [],
            "vars": {
                "ansible_ssh_private_key_file": "~/.ssh/test",
                "ansible_user": "root",
                "ansible_host_key_checking": False
            }
        }
    }

    for lease in leases:
        ip_address = lease["ip"]
        hostname = lease.get("hostname", "PC{}".format(ip_address.split('.')[-1]))
        inventory["leerlingen"]["hosts"].append(hostname)
        inventory["_meta"]["hostvars"][hostname] = {
            "ansible_host": ip_address,
            "ansible_ssh_private_key_file": "~/.ssh/test",
            "ansible_user": "root",
            "ansible_host_key_checking": False
        }

    return inventory

def main():
    inventory_data = generate_inventory_json()
    print(json.dumps(inventory_data, indent=4))

if __name__ == "__main__":
    main()
