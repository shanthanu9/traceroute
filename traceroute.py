import socket

HOST = 'google.com'
PORT = 5005 # some random port

def send_udp_packet(ttl):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        s.connect((HOST, PORT))
        s.send(b'UDP message!')

def capture_icmp_packet(ttl):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as icmp_soc:
        icmp_soc.settimeout(1) # Set wait time to be 1 second
        print(f'{ttl}: ', end='')

        try:
            (msg, addr) = icmp_soc.recvfrom(1024)
        except socket.timeout:
            print('ICMP msg not sent back in 1 second')
        else:
            print(addr[0])

if __name__ == '__main__':
    for ttl in range(1, 10):
        send_udp_packet(ttl)
        capture_icmp_packet(ttl)

