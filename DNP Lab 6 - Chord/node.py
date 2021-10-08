import time
from xmlrpc.server import SimpleXMLRPCServer
import threading
import xmlrpc.client


class Node(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.n = xmlrpc.client.ServerProxy(f'http://127.0.0.1:1239')
        self.finger_table = {}
        self.port = port
        self.id, self.message = self.n.register(port)
        self.start()

    def get_finger_table(self):
        requested_chord = self.n.get_chord_info()
        for i in self.finger_table:
            if i not in requested_chord:
                self.finger_table = self.n.populate_finger_table(self.id)
                break
        return self.finger_table

    def quit(self):
        status, message = self.n.deregister(self.id)
        return status, message

    def run(self):
        time.sleep(1)
        self.finger_table = self.n.populate_finger_table(self.id)
        node_server = SimpleXMLRPCServer(("127.0.0.1", self.port), logRequests=False)
        node_server.register_function(self.get_finger_table, 'get_finger_table')
        node_server.register_function(self.quit, 'quit')
        try:
            node_server.serve_forever()
        except KeyboardInterrupt:
            print("\nRegistry server is quitting ...")
            exit()
