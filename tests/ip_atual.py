import socket
from pprint import pprint as pp

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(("8.8.8.8", 80))

pp(s.getsockname()[0])
