import socket
import struct

HOST = 'iris.nitk.ac.in'
PORT = 5005 # some random port
ICMP_STRUCTURE_FMT = '!bbHHh'
ip_address = socket.gethostbyname(HOST)


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
            type,code,_,_,_=struct.unpack(ICMP_STRUCTURE_FMT,msg[20:28])
            print(struct.unpack(ICMP_STRUCTURE_FMT,msg[20:28]))
            if not (type==11 and code==0):
                print('ICMP received but not of packet sent')
        except socket.timeout:
            print('ICMP msg not sent back in 1 second')
        else:
            if(type == 11 and code == 0):
                if ip_address==addr[0]:
                    print('destination reached ',end='')
                    print(ip_address+' '+addr[0])
                    exit(1)
                else:
                    print(ip_address+' '+addr[0])

if __name__ == '__main__':
    for ttl in range(1, 200):
        send_udp_packet(ttl)
        capture_icmp_packet(ttl)

