
import socket
import sys
from _thread import *
from rsa import *
msgSz = 2048

active_clients = list()
public_keys_info = list()

def delete(connection):
    connection.close()
    if(connection in active_clients):
        active_clients.remove(connection)

def deletePBKey(ip_address):
    for pubKey in public_keys_info:
        if(pubKey['addr'] == ip_address):
            print(f'Removing public key info for {ip_address}')
            public_keys_info.delete(pubKey)

def broadcast_msg(msg, sender_conn):
    for client in active_clients:
        if(client['conn'] != sender_conn):
            try:
                client['conn'].send(msg.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting to {client['addr']}: {str(e)}")
                delete(client['conn'])
                deletePBKey(client['addr'])

def send_msg(msg, destAddr):
    for client in active_clients:
        if(client['addr'] == destAddr):
            try:
                client['conn'].send(msg.encode('utf-8'))
            except Exception as e:
                print(f"Error sending to {client['addr']}: {str(e)}")
                delete(client['conn'])
                deletePBKey(client['addr'])

def handleClient(conn, addr):
    is_connected = False
    current_connection = str()

    # send client IP that connect to server
    conn.send(str(addr[0]).encode('utf-8'))

    # get public key
    data = conn.recv(msgSz)
    data = data.decode('utf-8')
    pubKey = eval(data)

    #print(f"Public Key of {addr[0]}: {pubKey}")
    #print(f"Private Key of {addr[0]}: {prKey}")

    # send others public key to new client
    conn.send(str(public_keys_info).encode('utf-8'))

    data = {'pubKey': pubKey, 'addr': addr[0], 'is_connected': False}

    public_keys_info.append(data)

    # send new client's public key to other client
    data = {'type': 'pubkey', 'message': {'addr': addr[0], 'pubKey': pubKey, 'is_connected': False}}

    broadcast_msg(str(data), conn)

    while True:
        try:
            # if not connected
            if not is_connected:
                message = eval(conn.recv(msgSz).decode('utf-8'))

                if message:
                    # msg destination
                    if (message['dest']):
                        dest = message['dest']

                        # print(msg)
                        send_msg(str(message), dest)
                    # msg indicate client have been created a chat session
                    else:
                        is_connected = True
                        current_connection = message['addr']
                        print(f"{addr[0]} is chatting with {current_connection}")

                else:
                    delete(conn)
                    deletePBKey(addr[0])
            # if connected
            else:
                message = conn.recv(msgSz)
                message = message.decode('utf-8')
                ciphertext, length = message.split(',')
                if message:
                    print(f"Sender: {addr[0]}")
                    print(f"Message: {ciphertext}")
                    print('\n')
                    #print(f"Length: {length}\n")

                    send_msg(f"{addr[0]},{message}", current_connection)

                else:
                    delete(conn)
                    deletePBKey(addr[0])
        except Exception as e:
            continue

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('10.44.1.2', 55))
    server.listen(50)

    print("Server is ready for incoming connections...")
    try:
    # server accept connection request from each client
        while True:
            conn, addr = server.accept()

            active_clients.append({'conn': conn, 'addr': addr[0]})

            print(f"{addr[0]} has joined")

            start_new_thread(handleClient, (conn, addr))

    except KeyboardInterrupt:
        print("\nServer shutting down ...")

    finally:
        for client in active_clients:
            client['conn'].close()
        server.close()
