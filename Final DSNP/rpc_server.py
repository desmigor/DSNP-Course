from xmlrpc.server import SimpleXMLRPCServer

PORT = 12345
HOST = "127.0.0.1"
holder = []

# Create server
with SimpleXMLRPCServer((HOST, PORT), logRequests=False) as server:
    try:
        server.register_introspection_functions()


        def put(string: str):
            holder.append(string)
            return True
        server.register_function(put)


        def pick():
            return holder[0]


        server.register_function(pick)


        def pop():
            if len(holder) == 0:
                return "None"
            else:
                popping = holder[0]
                holder.pop(0)
                return popping


        server.register_function(pop)


        def size():
            return len(holder)


        server.register_function(size)

        # Running the server
        server.serve_forever()

    except KeyboardInterrupt:
        print("Server is stopping")
    exit(1)
