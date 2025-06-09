from napalm import get_network_driver as gnd

def get_interface(host: str, username: str, password: str) -> dict:
    """
    Retrieves interface status and configuration from network devices using NAPALM.
    
    Args:
        host (str): IP address or hostname of the target device
        username (str): SSH authentication username
        password (str): SSH authentication password
    
    Returns:
        dict: Nested dictionary containing interface details with structure:
              {
                  'InterfaceName': {
                      'is_up': bool,
                      'is_enabled': bool,
                      'speed': int,
                      ...
                  },
                  ...
              }
    
    Raises:
        ConnectionError: If device connection or authentication fails
    """
    # Initialize NAPALM driver for Cisco IOS devices
    driver = gnd('ios')
    
    try:
        # Establish connection using context manager for automatic cleanup
        with driver(hostname=host, username=username, password=password) as device:
            # Retrieve all interface details from device
            return device.get_interfaces()
    except Exception as e:
        # Re-raise with more contextual information
        raise ConnectionError(f"Failed to connect to {host}: {str(e)}")

if __name__ == '__main__':
    # Example usage - test connectivity and interface status
    try:
        ifaces = get_interface(
            host='192.168.199.20',
            username='admin',
            password='python'
        )
        
        # Display only active interfaces
        for iface_name, iface_data in ifaces.items():
            if iface_data['is_up'] and iface_data['is_enabled']:
                print(f"Interface {iface_name} is operational at {iface_data['speed']}bps")
                
    except ConnectionError as e:
        print(f"Error: {e}")
        exit(1)