from socket import *

IP_ADDR = '127.0.0.1'
PORT = 50505
DEST_PORT = 50505
BUF_SIZE = 1024

s = socket(AF_INET, SOCK_DGRAM)

s.bind((IP_ADDR, PORT))

print(f"Server is running on({IP_ADDR},{PORT})")

while True:
    try:
        data = s.recvfrom(BUF_SIZE)
        res = "hi"
        s.sendto(res.encode(), (IP_ADDR, DEST_PORT))



    except KeyboardInterrupt:
        print("Server stopped")
        exit(1)

