from socket import *
import time
import sys


class wrong_args(Exception):
    pass

try:
    # print(sys.argv)
    if len(sys.argv) != 3:
        raise wrong_args
    host = sys.argv[1]
    port = int(sys.argv[2])

except wrong_args:
    print("Usage example: python./client.py <address> <port>")
    exit()

with socket(AF_INET, SOCK_STREAM) as clientsocket:
    try:
        clientsocket.connect((host, port))
    except ConnectionRefusedError:
        print("Server is unavailable")
        exit()
    # Wait for a response, then print sent response to the console
    current_port = clientsocket.recv(1024)
    if current_port.decode('ascii') == '':
        print("Response is empty")
        exit(0)

    if current_port.decode('ascii') == 'The server is full':
        print("The server is Full")
        exit(0)

    with socket(AF_INET, SOCK_STREAM) as sock:
        time.sleep(1)
        sock.connect((host, int(current_port)))
        response = sock.recv(1024)
        print(response.decode('ascii'))
        # Entering range
        range_ok = False
        range = ""
        while not range_ok:
            range = input("Enter the range: \n")
            x = range.split()
            if len(x) == 2 and int(x[0]) < int(x[1]):
                range_ok = True

        # Sending the range minimum to the server
        sock.send(x[0].encode('ascii'))

        # Sending the range maximum to the server
        sock.send(x[1].encode('ascii'))

        while True:
            # Ask for user to guess a number
            attemptsresponse = sock.recv(1024)
            print(attemptsresponse.decode('ascii'))

            guess = input()
            # Format the guess, ready to send to the server
            # guessstring = "Guess: " + str(guess) + "\r\n"
            # Send the guess
            sock.send(guess.encode('ascii'))

            # Wait for the response from the server
            response = sock.recv(1024).decode('ascii')
            print(response)

            # Determine if the game is over
            if response == "You win!" or response == "You lose":
                break
