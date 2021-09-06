import random
from socket import *
import threading
import argparse

parser = argparse.ArgumentParser(usage='Usage example: python./server.py <port>',
                                 description='Starting game on a server')
parser.add_argument('port', type=int, help='port to run the server on')
args = parser.parse_args()

# Counter of connected clients
counter = 0

print(f"Starting the server on 127.0.0.1:{args.port}")


# Function definitions
def guessgame(clientsocket, clientaddress, port):
    global counter

    clientsocket.close()
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", port))
        sock.listen()
        clientsocket, clientaddress = sock.accept()
        # Send the welcome message to the client
        welcomemessage = "Welcome to the number guessing game!"
        clientsocket.send(welcomemessage.encode('ascii'))

        # clientsocket.send(port.encode())

        # Receiving the client's minimum range
        rangemin = clientsocket.recv(1024)

        # Receiving the client's maximum range
        rangemax = clientsocket.recv(1024)

        # print("The min range is " + rangemin.decode('ascii'))
        # print("The max range is " + rangemax.decode('ascii'))

        attempts = 5
        # Generate a random number for the client to try and guess
        numbertoguess = generatenumber(int(rangemin), int(rangemax))

        # Main loop
        while attempts >= 1:

            attemptsmessage = f"You have {attempts} attempts"
            clientsocket.send(attemptsmessage.encode('ascii'))
            guessstring = clientsocket.recv(1024)

            # Split the guess string up to get the integer guessed
            guess = int(guessstring)

            # If the player has guessed correctly
            if guess == numbertoguess:
                messagetosend = "You win!"
                clientsocket.send(messagetosend.encode('ascii'))
                # Close the connection
                clientsocket.close()
                print("Connection closed.")
                print("Waiting for a connection")
                counter -= 1
                exit()

            # Finding the message to send depending on the comparison between the guess and the numbertoguess
            elif guess < numbertoguess and attempts > 1:
                messagetosend = "Greater"
                # Send the response to the player
                clientsocket.send(messagetosend.encode('ascii'))

            elif guess > numbertoguess and attempts > 1:
                messagetosend = "Less"
                # Send the response to the player
                clientsocket.send(messagetosend.encode('ascii'))

            attempts -= 1
            if attempts == 0:
                messagetosend = "You lose"
                counter -= 1
                clientsocket.send(messagetosend.encode('ascii'))
                # Close the connection
                clientsocket.close()
                print("Connection closed.")
                print("Waiting for a connection")
                exit()


def generatenumber(x, y):
    return random.randrange(x, y)


# Main server loop
number_of_ports = 1
if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as serversocket:
        serversocket.bind(('127.0.0.1', args.port))
        serversocket.listen()
        while True:
            print("Waiting for a connection")
            (clientsocket, clientaddress) = serversocket.accept()
            print("Client connected")
            counter += 1
            if counter > 2:
                message = "The server is full"
                print(message)
                print("Waiting for a connection")
                clientsocket.sendall(message.encode())
                counter = 3
                clientsocket.close()
                while counter > 2:
                    pass
            else:
                clientsocket.sendall(str(args.port + number_of_ports).encode())
                t = threading.Thread(target=guessgame, args=(clientsocket, clientaddress, args.port + number_of_ports))
                number_of_ports += 1
                t.start()
