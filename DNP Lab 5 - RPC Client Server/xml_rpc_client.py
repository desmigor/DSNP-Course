import xmlrpc.client
import pickle
import sys
import os

try:
    host = sys.argv[1]
    port = int(sys.argv[2])
except Exception:
    print("Usage example: python./xml_rpc_client.py <address> <port>")
    exit()

s = xmlrpc.client.ServerProxy(f'http://{host}:{port}')

while True:
    try:
        command = input("\nEnter the command:\n")

        server_command = command.split()

        if server_command[0] == 'send':
            if not os.path.exists('./client_storage/' + server_command[1]):
                print("Not completed")
                print("File doesn't exist")
            else:
                with open('./client_storage/' + server_command[1], 'rb') as f:
                    binary_data = pickle.dumps(f.read())
                    response = s.send(server_command[1], binary_data)
                if response == True:
                    print("Completed")
                else:
                    print("Not completed")
                    print("File already exists")

        elif server_command[0] == 'list':
            response = s.list()
            print("\n".join(response))
            print("Completed")

        elif server_command[0] == 'delete':
            response = s.delete(server_command[1])
            if response == True:
                print("Completed")
            else:
                print("Not completed")
                print("No such file")

        elif server_command[0] == 'get':
            check, binary_data = s.get(server_command[1])
            # If the new name is not provided
            if len(server_command) == 2:
                if os.path.exists("./client_storage/" + server_command[1]):
                    print("Not completed")
                    print("File already exists")

                elif check == False:
                    print("Not completed")
                    print("File doesn't exist on the server")

                elif check == True:
                    with open(f"./client_storage/{server_command[1]}", 'wb') as file:
                        file.write(pickle.loads(binary_data.data))
                        print("Completed")

            # if the new name is provided
            elif len(server_command) == 3:

                if os.path.exists("./client_storage/" + server_command[2]):
                    print("Not completed")
                    print("File already exists")

                elif check == False:
                    print("Not completed")
                    print("File doesn't exist on the server")
                elif check == True:
                    with open(f"./client_storage/{server_command[2]}", 'wb') as file:
                        file.write(pickle.loads(binary_data.data))
                        print("Completed")


        elif command == "quit":
            print("Client is stopping")
            exit()
        elif server_command[0] == 'calc':
            response, correct = s.calc(command)
            if response == True and correct == True:
                print("Correct comparison")
                print("Completed")
            elif response == False and correct == True:
                print("Incorrect comparison")
                print("Completed")
            elif correct:
                print(int(response))
                print("Completed")
            else:
                print("Not completed")
                print(response)

        else:
            print("Not completed\nWrong command\n")

    except KeyboardInterrupt:
        print("Server is stopping")
        exit()
    except ConnectionRefusedError:
        print("Server not available")
        exit()
    except IndexError:
        print("Not completed\nWrong command\n")