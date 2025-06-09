from netmiko import ConnectHandler
import re

class ARPRetriever:
    """
    A class to retrieve and parse ARP table entries from network devices via SSH.
    Uses Netmiko for SSH connectivity and regex for parsing.
    
    Args:
        host (str): IP address or hostname of the network device.
        username (str): SSH username for authentication.
        password (str): SSH password for authentication.
        device_type (str, optional): Netmiko device type (default: 'cisco_ios').
    """

    def __init__(self, 
                host: str,
                username: str,
                password: str,
                device_type: str = 'cisco_ios'):
        """
        Initializes the SSH connection to the network device using Netmiko.
        """
        # Establish an SSH connection to the device
        self.connection = ConnectHandler(
            host=host,
            username=username,
            password=password,
            device_type=device_type
        )

    def get_arp_table(self):
        """
        Retrieves and parses the ARP table from the device.
        
        Returns:
            list: A list of dictionaries, each containing:
                - 'ip' (str): IP address
                - 'mac' (str): MAC address
                - 'interface' (str): Interface name
        
        Example Output:
            [{'ip': '192.168.1.1', 'mac': 'aabb.cc00.0110', 'interface': 'Ethernet0/1'}, ...]
        """
        # Send the CLI command to get ARP table
        command = self.connection.send_command('show ip arp')
        arp_entries = []

        # Regex patterns to extract IP, MAC, and Interface from ARP table
        # Sample ARP entry: 
        # "Internet  192.168.1.1   10   aabb.cc00.0110  ARPA  Ethernet0/1"
        ip_regex = r'(\d+\.\d+\.\d+\.\d+)'  # Matches IPv4 address
        mac_regex = r'([a-fA-F0-9]{4}\.){2}[a-fA-F0-9]{4}'  # Matches Cisco-style MAC (e.g., aabb.cc00.0110)
        interface_regex = r'(\S+)$'  # Matches the last non-whitespace field (interface)

        # Parse each line of the ARP table
        for line in command.splitlines():
            ip_match = re.search(ip_regex, line)
            mac_match = re.search(mac_regex, line)
            interface_match = re.search(interface_regex, line)

            # Only append valid entries (all 3 fields present)
            if ip_match and mac_match and interface_match:
                arp_entries.append({
                    'ip': ip_match.group(0),
                    'mac': mac_match.group(0),
                    'interface': interface_match.group(0)
                })

        return arp_entries


if __name__ == '__main__':
    """
    Example usage for testing the ARPRetriever class.
    """
    # Initialize the ARPRetriever with device credentials
    arp_entry = ARPRetriever(
        host='192.168.199.20',
        username='admin',
        password='python'
    )

    # Fetch and parse the ARP table
    arp_table = arp_entry.get_arp_table()

    # Pretty-print each ARP entry
    for entry in arp_table:
        print(f"{entry['ip']} => {entry['mac']} on {entry['interface']}")