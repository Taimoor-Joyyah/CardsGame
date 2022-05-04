import socket


def validinput(prompt):
    while True:
        get = input(prompt)
        if get:
            return get
        else:
            print("invalid input")


s = socket.socket()

address = validinput('Enter Host Address : ')
port = int(validinput('Enter Host Port : '))

s.connect((address, port))

s.send(validinput('Enter nickname : ').encode())

while True:
    option = s.recv(1024).decode()
    if option.isnumeric():
        s.send('3'.encode())
    message = s.recv(1024).decode()
    if option == '0':
        print(message)
        s.send('4'.encode())
    elif option == '1':
        s.send(validinput(message).encode())
    elif option == '2':
        break

s.close()
