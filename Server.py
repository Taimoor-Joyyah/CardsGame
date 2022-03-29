import socket


class Client:
    def __init__(self, client):
        self.socket = client[0]
        self.address = client[1]


port = 40674
server = socket.socket()
server.bind(('', port))
server.listen()

print(f"Server is Connected on {socket.gethostbyname(socket.gethostname())}:{port}")

host_player = 0
clients = []
nicknames = []


def connect_host_player():
    clients.append(Client(server.accept()))
    nicknames.append(clients[0].socket.recv(1024).decode())
    print(f'Player 0 (HOST) ({nicknames[0]}) is connected at address {clients[0].address[0]}:{clients[0].address[1]}')


def connect_players(players):
    print('Listening players to connect')
    for player in range(1, players):
        clients.append(Client(server.accept()))
        nicknames.append(clients[player].socket.recv(1024).decode())
        print(f'Player {player} ({nicknames[player]}) is connected at address '
              f'{clients[player].address[0]}:{clients[player].address[1]}')
    print('All players are connected')


def send_message(players, message):
    for player in players:
        clients[player].socket.send('0'.encode())
        if clients[player].socket.recv(1024).decode().isnumeric():
            clients[player].socket.send(message.encode())


def receive_message(player, message):
    print(f'Listening player {nicknames[player]}....')
    clients[player].socket.send('1'.encode())
    if clients[player].socket.recv(1024).decode().isnumeric():
        clients[player].socket.send(message.encode())
    return clients[player].socket.recv(1024).decode()


def close_connections():
    for index, client in enumerate(clients):
        clients[index].socket.send('2'.encode())
        client.socket.close()
