import socket

s = socket.socket()

address = input('Enter Host Address : ')
port = int(input('Enter Host Port : '))

s.connect((address, port))

s.send(input('Enter nickname : ').encode())

while True:
    option = s.recv(1024).decode()
    if option.isnumeric():
        s.send('1'.encode())
    message = s.recv(1024).decode()
    if option == '0':
        print(message)
    elif option == '1':
        s.send(input(message).encode())
    elif option == '2':
        break

s.close()
