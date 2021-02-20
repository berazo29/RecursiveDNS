import argparse
from sys import argv
import socket


parser = argparse.ArgumentParser(description="""Top Server """)
parser.add_argument('-f', type=str, help='File to read for top server', default='PROJI-DNSTS.txt', action='store', dest='in_file')
parser.add_argument('port', type=int, help='This is the server port to listen', action='store')
args = parser.parse_args(argv[1:])

# load the text file as dictionary

index_pairs = {}
with open(args.in_file) as f:
    for line in f:
        (key, val) = line.strip().split(':')
        index_pairs[key] = val

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

# accept a client
csockid, addr = ss.accept()
print("[S]: Got a connection request from a client at {}".format(addr))

with csockid:
    while True:
        data = csockid.recv(512)
        data = data.decode('utf-8')

        try:
            if index_pairs[data]:
                print('[C]: {}'.format(data))
                print('[S]: {}'.format(index_pairs[data]))
                csockid.sendall(index_pairs[data].encode('utf-8'))

        except:
            if not data:
                break
            answer = 'NOT FOUND'
            print('[C]: {}'.format(data))
            print('[S]: {}'.format(answer))
            csockid.sendall(answer.encode('utf-8'))
ss.close()
exit()

