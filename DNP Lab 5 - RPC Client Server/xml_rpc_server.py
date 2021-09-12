import os
from xmlrpc.server import SimpleXMLRPCServer
import sys
import pickle

try:
    host = sys.argv[1]
    port = int(sys.argv[2])
except Exception:
    print("Usage example: python./xml_rpc_server.py <address> <port>")
    exit()

# Create server
with SimpleXMLRPCServer((host, port), logRequests=False) as server:

    try:
        server.register_introspection_functions()


        def send_file(filename, data):
            check = False
            if os.path.exists("./server_storage/" + filename):
                print(filename + " not saved")
            else:
                with open(f"./server_storage/{filename}", 'wb') as file:
                    file.write(pickle.loads(data.data))
                    check = True
                    print(filename + " saved")
            return check


        server.register_function(send_file, 'send')


        def list_files():
            return os.listdir("./server_storage")

        server.register_function(list_files, 'list')


        def delete_files(filename):
            check = False
            if not os.path.exists("./server_storage/" + filename):
                print(filename + " not deleted")
            else:
                os.remove(f"./server_storage/{filename}")
                check = True
                print(filename + " deleted")
            return check

        server.register_function(delete_files, 'delete')


        def get_file(filename):
            check = False
            file = ""
            if not os.path.exists("./server_storage/" + filename):
                print("No such file: " + filename)
            else:
                with open('./client_storage/' + filename, 'rb') as f:
                    file = pickle.dumps(f.read())
                    check = True
            return check, file

        server.register_function(get_file, 'get')


        def calculate(expression):
            check = False
            exp = expression.split()
            operator = exp[1]
            num1 = exp[2]
            num2 = exp[3]
            if operator == '+':
                answ = int(num1) + int(num2)
                check = True
                print(expression + " -- done")
                return answ, check

            elif operator == '-':
                answ = int(num1) - int(num2)
                check = True
                print(expression + " -- done")
                return answ, check

            elif operator == '*':
                answ = int(num1) * int(num2)
                check = True
                print(expression + " -- done")
                return answ, check

            elif operator == '/':
                try:
                    answ = int(num1) / int(num2)
                    check = True
                    print(expression + " -- done")
                except ZeroDivisionError:
                    print(expression + " -- not done")
                    return "Division by zero", check
                return answ, check

            elif operator == '>':
                answ = int(num1) > int(num2)
                check = True
                print(expression + " -- done")
                return answ, check

            elif operator == '<':
                answ = int(num1) < int(num2)
                check = True
                print(expression + " -- done")
                return answ, check

            elif operator == '>=':
                answ = int(num1) >= int(num2)
                check = True
                print(expression + " -- done")
                return answ, check

            elif operator == '<=':
                answ = int(num1) <= int(num2)
                check = True
                print(expression + " -- done")
                return answ, check

            else:
                print(expression + " -- not done")
                return "wrong operation", check


        server.register_function(calculate,'calc')

        # Running the server
        server.serve_forever()

    except KeyboardInterrupt:
        print("Server is stopping")
    sys.exit(0)
