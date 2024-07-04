import socket
import select

HEADER_LENGHT = 10
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 6969
ADDR = (SERVER, PORT)
FORMATE = "utf-8"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(ADDR)
server_socket.listen()

sockets_list = [server_socket]

clients = {}

def startup():
    print(f"""
**********************************************************
*                                                        *
*                *** SERVER STARTING ***                 *
*                                                        *
**********************************************************
Server Address: {SERVER}
Server Port: {PORT}
Waiting for connections...
**********************************************************
""")

startup()

def receive_message(client_socket):

    try:
        message_header = client_socket.recv(HEADER_LENGHT)

        if not len(message_header):
            return False

        message_lenght = int(message_header.decode(FORMATE).strip()) #strip is not needed so can be removed in pyhton
        return {"header": message_header, "data": client_socket.recv(message_lenght)}

    except:
        return False
    

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list) #read write error sockets

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accepted a new connection from {client_address[0]} : {client_address[1]} username:{user['data'].decode(FORMATE)}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode(FORMATE)}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode(FORMATE)}: {message['data'].decode(FORMATE)}") #see '' in formate type

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data']) #by this we can display both useranme and message


    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

