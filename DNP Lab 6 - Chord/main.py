import xmlrpc.client
import sys
from registry import Registry as R
from node import Node


try:
    m = int(sys.argv[1])  # length of identifiers in chord (in bits) - Default value=5
    first_port = int(sys.argv[2])
    last_port = int(sys.argv[3])

except IndexError:
    print("Usage example: python main.py <address> <port>")
    exit()
except Exception as e:
    print(e)
    exit()

reg = R(m)
nodes = [Node(i) for i in range(first_port, last_port+1)]

node_server = []
for i in range(first_port, last_port+1):
    node_server.append(xmlrpc.client.ServerProxy(f'http://127.0.0.1:{i}'))

# print(node_server)
reg_server = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1239')

print("Registry and 5 nodes are created.\n")
while True:
    try:
        command = input()
        client_command = command.split()

        if client_command[0] == 'get_chord_info':
            chord_info = reg_server.get_chord_info()
            print(chord_info)
            print()

        elif client_command[0] == 'get_finger_table':
            ft_dict = node_server[int(client_command[1])-first_port].get_finger_table()
            print(ft_dict)
            print()

        elif client_command[0] == 'quit':
            status, message = node_server[int(client_command[1])-first_port].quit()
            print(message)
            print()

        else:
            print("Not completed. Wrong command\n")

    except KeyboardInterrupt:
        print("\nClient is quitting ...")
        exit()
    except ConnectionRefusedError:
        print("Node Server not available")
        exit()
    except IndexError:
        print("Not completed. Wrong command\n")
