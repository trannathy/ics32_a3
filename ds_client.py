# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# THYNT1
# THYNT1@UCI.EDU
# 90526048
import socket
from collections import namedtuple
import ds_protocol


Connection = namedtuple('Connection', ['socket', 'send', 'recv'])

class DSUServerError(Exception):
    pass


def send(server: str, port: int, username: str, password: str, message: str, bio: str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    try:
        connection = connect_to_server(server, port)
    
    except DSUServerError:
        return False
    
    else:
        print("SUCESSFULLY CONNECTED TO THE SERVER!")
        send_join(connection, username, password)
        svr_type, user_token = interpret_svr_msg(connection)

        if (svr_type != "error" and svr_type is not None) and message != "":
            send_post(connection, message, user_token)
            svr_type, token_catch = interpret_svr_msg(connection)

        elif (svr_type != "error" and svr_type is not None) and bio is not None:
            send_bio(connection, bio, user_token)
            svr_type, token_catch = interpret_svr_msg(connection)
        
        disconnect(connection)

        if svr_type == "error" or svr_type is None:
            return False
        else:
            return True


def send_join(conn: Connection, user: str, pwd: str):
    join_msg = ds_protocol.create_join_msg(user, pwd)
    write_to_svr(conn, join_msg)


def send_post(conn: Connection, entry: str, token: str):
    post_msg = ds_protocol.create_post_msg(entry, token)
    write_to_svr(conn, post_msg)


def send_bio(conn: Connection, new_bio:str, token: str):
    bio_msg = ds_protocol.create_bio_msg(new_bio, token)
    write_to_svr(conn, bio_msg)


def connect_to_server(host: str, port: int):
    try:
        print(f"Connecting to host {host} at port {port}")
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((host, port))

        connection = make_connection(my_socket)
        return connection
  
    except ConnectionRefusedError or ConnectionError or ConnectionAbortedError:
        print("COULD NOT CONNECT TO THE DSU SERVER.")
        raise DSUServerError
   

def disconnect(conn: Connection):
    conn.send.close()
    conn.recv.close()
    conn.socket.close()
    print("DISCONNECTED")


def write_to_svr(conn:Connection, message_to_send:str):
    try:
        conn.send.write(message_to_send + "\n")
        conn.send.flush()

    except:
        raise DSUServerError("COULD NOT SEND MESSAGE TO THE SERVER")


def make_connection(sock:socket) -> Connection:
    f_send = sock.makefile('w')
    f_recv = sock.makefile('r')

    return Connection(socket = sock, send = f_send, recv = f_recv)


def read_message(conn:Connection) -> str:
    try:
        received = conn.recv.readline()[:-1]
        return received
    except:
        raise DSUServerError


def interpret_svr_msg(conn: Connection) -> tuple:
    try:
        svr_msg = ds_protocol.extract_json(read_message(conn))
        print_svr_msg(svr_msg.type, svr_msg.message)
        return svr_msg.type, svr_msg.token

    except DSUServerError or TypeError:
        print("ERROR: COULD NOT READ SERVER MESSGAE")
        return None, None



def print_svr_msg(type, msg) -> str:
    if type == "error":
        print(f"ERROR:")
    
    if msg is not None:
        print(msg)
