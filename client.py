import socket
import errno
import sys
import threading

HEADER = 10
IP = socket.gethostbyname(socket.gethostname())
PORT = 6969
FORMATE = "utf-8"


my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))
client_socket.setblocking(False) #by this recv function will not be blocking

username = my_username.encode(FORMATE)
username_header = f"{len(username):< {HEADER}}".encode(FORMATE)
client_socket.send(username_header + username)

def startup():
    print("""
**********************************************************
*                                                        *
*                *** CLIENT STARTING ***                 *
*                                                        *
**********************************************************
""")

startup()

def send_message(client_socket):
    while True:
        message = input(f"[{my_username}] >>> ")    
        if message:
            message = message.encode(FORMATE)
            message_header = f"{len(message):<{HEADER}}".encode(FORMATE)
            client_socket.send(message_header + message)


def receive_message():
    while True:
        try:
            username_header = client_socket.recv(HEADER)
            if not len(username_header):
                print("Connection closed by server...")
                sys.exit()

            username_lenght = int(username_header.decode(FORMATE).strip())
            username = client_socket.recv(username_lenght).decode(FORMATE)

            message_header = client_socket.recv(HEADER)
            message_lenght = int(message_header.decode(FORMATE).strip())
            message = client_socket.recv(message_lenght).decode(FORMATE)

            sys.stdout.write('\r' + ' ' * (len(my_username) + len(message) + 6) + '\r')
            print(f"[{username}] >>> {message} ")
            sys.stdout.write(f"[{my_username}] >>> ")
            sys.stdout.flush()
        
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
            continue
        except Exception as e:
            print('General error', str(e))
            sys.exit()


send_thread = threading.Thread(target=send_message, args=(client_socket,))
receive_thread = threading.Thread(target=receive_message)

send_thread.start()
receive_thread.start()
