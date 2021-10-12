import xmlrpc.client

PORT = 12345
HOST = "127.0.0.1"

s = xmlrpc.client.ServerProxy(f'http://{HOST}:{PORT}')

while True:
    try:
        command = input("Enter the command:")

        server_command = command.split()

        if server_command[0] == 'put':
            s.put(str(server_command[1]))

        elif server_command[0] == 'pick':
            response = s.pick()
            print(response)

        elif server_command[0] == 'pop':
            response = s.pop()
            print(response)

        elif server_command[0] == 'size':
            response = s.size()
            print(response)

        else:
            print("Not completed\nWrong command\n")

    except KeyboardInterrupt:
        print("\nClosing")
        exit()
    except ConnectionRefusedError:
        print("Server not available")
        exit()
    except IndexError:
        print("Not completed\nWrong command\n")