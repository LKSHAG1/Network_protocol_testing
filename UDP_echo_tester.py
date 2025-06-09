import re
import subprocess
import socket

class UDP_echo_tester:
    """
    A class to test UDP echo functionality and basic ping stats.
    
    Methods:
    - send_and_receive: sends a UDP message and waits for the echo reply.
    - ping: runs the system ping command and parses packet loss & RTT.
    """
    def __init__(self, 
                 src_ip : str = '192.168.1.4',
                 src_port : int = 1233,
                 dst_ip : str = '8.8.8.8',
                 dst_port :int =  53
                 ):
        
        # Create a UDP socket and bind to the source IP/port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dst = (dst_ip, dst_port)
        self.sock.bind((src_ip, src_port))
        
        # Set a timeout so recvfrom() won’t block indefinitely
        self.sock.settimeout(2)

    def send_and_receive(self, message: str):
        """
        Sends `message` via UDP to dst_ip:dst_port,
        then waits for and returns the echoed reply.
        """
        #encode the message to bytes
        try:
            self.sock.sendto(message.encode(), self.dst)
            data, addr = self.sock.recvfrom(1024)
            return data.decode() #decode the bytes to string
        except socket.timeout:
            return "No response (timeout)" 
        

    def ping(self, packet_size :int  = 100, count :int = 10 ):
        """
        Runs the system `ping` command:
        - packet_size: payload bytes per ping
        - count: number of echo requests
        Parses output for packet loss (%) and average RTT (ms).
        """
        # Build the ping command (Linux/macOS variant)
        cmd = ['ping', '-n', str(count), '-l', str(packet_size), self.dst[0]]
        out = subprocess.check_output(cmd, text=True)

        #extracting the packet loss and RTT from the output
        #sample line - Packets: Sent = 1, Received = 0, Lost = 1 (100% loss)
        packet_loss_regex = r'\((\d+)% loss\)'
        loss_match = re.search(packet_loss_regex, out).group(1)
        
        #sample line Approximate round trip times in milli-seconds: Minimum = 3ms, Maximum = 3ms, Average = 3ms
        RTT_regex = r'Average = (\d+)ms'
        RTT_match = re.search(RTT_regex, out).group(1)

        return { 
            'packet_loss': loss_match,
            'avg_RTT' : RTT_match
        }

if __name__ == '__main__':
    #example usage of the UDP_echo_tester class
    tester = UDP_echo_tester()

    #Test UDP echo functionality
    echo = tester.send_and_receive("Hello, UDP Echo!")
    print(f'Echo reply: {echo}')

    #Test ping functionality
    ping_test = tester.ping(packet_size=4, count=5)
    print(f"Packet Loss: {ping_test['packet_loss']}%")
    print(f"Average RTT: {ping_test['avg_RTT']} ms")