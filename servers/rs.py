import argparse
from sys import argv
import socket


parser = argparse.ArgumentParser(description="""Root Server""")
parser.add_argument('-f', type=str, help='File to read for root server', default='PROJI-DNSRS.txt', action='store', dest='in_file')
parser.add_argument('port', type=int, help='This is the root server port to listen', action='store')
# parser.add_argument('next_port', type=int, help='This is the top server port to listen', action='store')
args = parser.parse_args(argv[1:])
print(args)

# load the text file with the ip addresses as dictionary
ip_addresses = {}
with open(args.in_file) as f:
    for line in f:
        (key, ip, flag) = line.strip().split(' ')
        key = key.lower()
        ip_addresses[key] = sorted({ip, flag})
# print(ip_addresses)

# Find next server ip address
thostname = ''

for record in ip_addresses:
    if ip_addresses[record][1] == 'NS':
        thostname = record + ' ' + 'NS'

# print(thostname)

# Create a new socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")

except socket.error as error:
    print("Server socket error: {}".format(error))
    exit()

server_addr = ('', args.port)
ss.bind(server_addr)
ss.listen(1)

# print server info
host = socket.gethostname()
print("[S]: Server hostname is {}".format(host))
localhost_ip = socket.gethostbyname(host)
print("[S]: Server IP address is {}".format(localhost_ip))
print("[S]: Server port number is {}".format(args.port))


while True:

    # accept a client
    csockid, addr = ss.accept()
    print("[S]: Got a connection request from a client at {}".format(addr))

    with csockid:
        while True:
            data = csockid.recv(512)
            data = data.decode('utf-8')

            try:
                if ip_addresses[data] and ip_addresses[data][1] != 'NS':
                    print('[C]: {}'.format(data))
                    print('[S]: {}'.format(ip_addresses[data]))
                    csockid.sendall(str(ip_addresses[data][0]+' '+ip_addresses[data][1]).encode('utf-8'))
                else:
                    csockid.sendall(str(thostname).encode('utf-8'))


            except:
                if not data:
                    break
                res_localhost = thostname
                print('[C]: {}'.format(data))
                print('[S]: {}'.format(res_localhost))
                csockid.sendall(str(res_localhost).encode('utf-8'))
# ss.close()
# exit()