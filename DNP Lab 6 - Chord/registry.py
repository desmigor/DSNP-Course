import threading
from xmlrpc.server import SimpleXMLRPCServer
import random


class Registry(threading.Thread):
    random.seed(0)

    def __init__(self, m):
        threading.Thread.__init__(self)
        self.m = m
        self.chord_dict = {}
        self.start()

    def register(self, port):
        id = random.randint(0, pow(2, self.m)-1)
        while id in self.chord_dict:
            id = random.randint(0, pow(2, self.m) - 1)
        self.chord_dict[str(id)] = port
        return id, "Node Registered successfully"

    def deregister(self, id):
        if str(id) not in self.chord_dict:
            return False, "This ID doesn't Exist"
        self.chord_dict.pop(str(id), None)
        return True, "Successfully removed"

    def get_chord_info(self):
        return self.chord_dict

    def populate_finger_table(self, id):
        ft = {}
        for i in range(0, self.m):
            val = (int(id) + 2**(i)) % 2**self.m
            res = 2**self.m
            for x in self.chord_dict:
                if val <= int(x) < res:
                    res = int(x)
            ft[str(res)] = self.chord_dict[str(res)]
        return ft

    def run(self):
        reg_server = SimpleXMLRPCServer(("127.0.0.1", 1239), logRequests=False)
        reg_server.register_function(self.register, 'register')
        reg_server.register_function(self.deregister, 'deregister')
        reg_server.register_function(self.get_chord_info, 'get_chord_info')
        reg_server.register_function(self.populate_finger_table, 'populate_finger_table')

        # Running the server
        try:
            reg_server.serve_forever()
        except KeyboardInterrupt:
            print("\n Registry server is quitting ...")
            exit()
