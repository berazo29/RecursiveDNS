import argparse
from sys import argv
import socket

#First we use the argparse package to parse the aruments
parser = argparse.ArgumentParser(description="""This is a client program""")
parser.add_argument('-f', type=str, help='This is the client file with the ip addresses', default='PROJI-HNS.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination with the servers responds', default='results.txt',action='store', dest='out_file')
parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',action='store')
parser.add_argument('rport', type=int, help='This is the port to connect to the server on',action='store')
parser.add_argument('tport', type=int, help='This is the port to connect to the server on',action='store')
args = parser.parse_args(argv[1:])

print(args)

#next we create a client socket
try:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

server_addr = (args.server_location, args.rport)
client_sock.connect(server_addr)


#now we need to open both files
with open(args.out_file, 'w') as write_file:
	for line in open(args.in_file, 'r'):
		#trim the line to avoid weird new line things
		line = line.strip('\n')
		print('[C]: {}'.format(line))
		#now we write whatever the server tells us to the out_file
		if line:
			client_sock.sendall(line.encode('utf-8'))
			answer = client_sock.recv(512)
			#decode answer
			answer = answer.decode('utf-8').split(' ')
			# print("[RS]: {}".format(answer))
			if answer[1] == 'A':
				print("[RS]: {}".format(answer))

			elif answer[1] == 'NS':

				try:
					next_client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					print("[C]: Create new second socket")
				except socket.error as err:
					print('socket open error: {} \n'.format(err))
					exit()

				next_server_addr = (answer[0], args.tport)
				next_client_sock.connect(next_server_addr)
				send = answer[0]

				if send:
					next_client_sock.sendall(line.encode('utf-8'))
					root_response = next_client_sock.recv(512)
					root_response = root_response.decode('utf-8').split(' ')
					print("[TS]: {}".format(root_response))
				next_client_sock.close()
				print("[C]: Client for second closed")




#close the socket (note this will be visible to the other side)
client_sock.close()
