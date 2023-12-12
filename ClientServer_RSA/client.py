# Python program to implement client side of chat room.
import socket
import select
import sys
import signal
from des import *
from rsa import *
msgSz = 2048
maxNum = 1000000000

# list of other client's and its public keys
clients = []

# connection status, true if client is in a chat session
connected = False
currConnected = str()

key = str()
ipClient = str()

# search pubkeys
def findPBKeys(addr):
    for client in clients:
        if(client['addr'] == addr):
            return client['pubKey']

def signal_handler(sig, frame):
    print('\nClosing client...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('10.44.1.2', 55))

    # get IP that connect to server
    ipClient = server.recv(msgSz).decode('utf-8')

    # send public key
    server.send(str(pubKey).encode('utf-8'))

    # get all client's public key from server
    clientList = server.recv(2048).decode('utf-8')
    clients = eval(clientList)
    print(f"List of clients:")
    # client belum ada
    if(len(clients) == 0):
        print("No client connect")
    # client ada
    else:
        for i in range(len(clients)):
            print(f"{i+1}. {clients[i]['addr']}")
        print("Who do you want to chat with?\n")

    while True:
        sockets_list = [sys.stdin, server]

        read_sockets, write_socket, error_socket = select.select(
            sockets_list, [], [])

        for socks in read_sockets:

            # client is not in chat session
            if not connected:
                if socks == server:
                    data = eval(socks.recv(msgSz).decode('utf-8'))

                    # new client's public key
                    if (data['type'] == "pubkey"):
                        clients.append(data['message'])
                        print(f"Client {data['message']['addr']} connected")
                        print(f"List of clients:")
                        # client belum ada
                        if(len(clients) == 0):
                            print("No client connects")
                        # client ada
                        else:
                            for i in range(len(clients)):
                                print(f"{i+1}. {clients[i]['addr']}")
                            print("Who do you want to chat with?\n")

                    # there is other client want to connect
                    elif (data['type'] == "initiator"):
                        print(data['src'] + " want to chat with you, accept? (yes/no)")
                        ans = input()

                        # invalid input
                        while(ans != "yes" and ans != "no"):
                            print("Invalid input, enter \"yes\" atau \"no\"")
                            ans = input()

                        # reject
                        if(ans == "no"):
                            data = {"type": "responder", "dest": data['src'], "src": ipClient, "message": "reject"}

                            server.send(str(data).encode('utf-8'))
                        # accept
                        else:
                            reply = {"type": "responder", "dest": data['src'], "src": ipClient, "message": "accept"}

                            server.send(str(reply).encode('utf-8'))
                            
                            tempPBKey = findPBKeys(data['src'])
                            tempPBKey = tempPBKey[0]

                            # menerima N1 dan IdA
                            msg = server.recv(msgSz).decode('utf-8')
                            msg = eval(msg)
                            N1, IdA = msg['message'].split(',')
                            N1 = rsa_decrypt(N1, prKey)
                            print(f"Received N1: {N1}\n")
                            IdA = rsa_decrypt(IdA, prKey)
                            print(f"Received ID: {IdA}\n")

                            # kirim N1 dan N2
                            N2 = random.randint(0, maxNum)
                            N2 = str(N2)
                            print(f"Sending  N1: {N1}")
                            N1 = rsa_encrypt(N1, tempPBKey)
                            print('\n')

                            print(f"Sending  N2: {N2}")
                            N2 = rsa_encrypt(N2, tempPBKey)
                            print('\n')

                            msg = f"{N1},{N2}"
                            n1n2 = {'dest': data['src'], 'src': ipClient, 'message': msg}

                            server.send(str(n1n2).encode('utf-8'))

                            # menerima N2
                            N2 = rsa_decrypt(eval(server.recv(msgSz).decode('utf-8'))['message'], prKey)
                            print(f"Received N2: {N2}")
                            print('\n')

                            # kirim session key
                            key = generateSessionKey()
                            print(f"Sending  key: {key}")
                            encKey = rsa_encrypt(key, tempPBKey)
                            keyData = {'dest': data['src'], 'src': ipClient, 'message': encKey}
                            print('\n')

                            server.send(str(keyData).encode('utf-8'))

                            # Koneksi berhasil
                            connected = True
                            currConnected = data['src']
                            connectionMessage = {'dest': None, 'addr': currConnected}

                            server.send(str(connectionMessage).encode('utf-8'))
                            print(f"Success to connect with {currConnected}")
                            print(f"Chat has been started with session key = {key}\n")

                    # another client send reply connection
                    elif (data['type'] == "responder"):
                        # client accept
                        if(data["message"] == "accept"):
                            # mencari public key client
                            tempPBKey = findPBKeys(data['src'])
                            tempPBKey = tempPBKey[0]

                            # kirim N1 dan Id A
                            N1 = random.randint(0, maxNum)
                            N1 = str(N1)

                            print(f"Sending  N1: {N1}")
                            N1 = rsa_encrypt(N1, tempPBKey)
                            print('\n')

                            print(f"Sending  ID: {ipClient}")
                            IdA = rsa_encrypt(ipClient, tempPBKey)
                            print('\n')

                            msg = f"{N1},{IdA}"
                            n1Id = {'dest': data['src'], 'src': ipClient, 'message': msg}

                            server.send(str(n1Id).encode('utf-8'))

                            # menerima N1, N2
                            N1, N2 = eval(server.recv(msgSz).decode('utf-8'))['message'].split(',')
                            N1 = rsa_decrypt(N1, prKey)

                            print(f"Received N1: {N1}")
                            print('\n')

                            N2 = rsa_decrypt(N2, prKey)
                            print(f"Received N2: {N2}")
                            print('\n')

                            # kirim N2
                            print(f"Sending  N2: {N2}")
                            N2 = rsa_encrypt(N2, tempPBKey)
                            print('\n')

                            n2 = {'dest': data['src'], 'src': ipClient, 'message': N2}

                            server.send(str(n2).encode('utf-8'))

                            # menerima N1 dan session Key
                            key = rsa_decrypt(eval(server.recv(msgSz).decode('utf-8'))['message'], prKey)

                            print(f"Received key: {key}")
                            print('\n')

                            # koneksi berhasil
                            connected = True
                            currConnected = data['src']
                            connectionMessage = {'dest': None, 'addr': currConnected}

                            server.send(str(connectionMessage).encode('utf-8'))
                            print(f"Success to connect with {currConnected}")
                            print(f"Chat has been started with session key = {key}\n")
                        # client reject
                        elif(data["message"] == "reject"):
                            print(f"{data['src']} reject connection")

                # try to connect to other client
                else:
                    selectedClient =int(input())

                    # invalid input
                    while(selectedClient<1 or selectedClient>len(clients)):
                        print("Invalid Input")
                        print("Who do you want to chat with?")
                        selectedClient = input("> ")

                    data = {'type': 'initiator', 'src': ipClient, 'dest': clients[selectedClient-1]['addr']}

                    server.send(str(data).encode('utf-8'))

                    print('Waiting for response..')


            # client is in chat session
            else:
                if socks == server:
                    addr, ciphertext, length = socks.recv(2048).decode('utf-8').split(',')
                    length = int(length)

                    plaintext = decrypt(ciphertext, key, length)
                    print(f"From: {addr}")
                    print(f"Encrypted Message: { ciphertext }")
                    print(f"Message: { plaintext }\n")
                    sys.stdout.flush()
                else:
                    plaintext = input()
                    # if user exit chat session
                    if(plaintext == 'exit'):
                        pass
                    ciphertext = encrypt(plaintext, key)

                    message = f"{ciphertext},{len(plaintext)}"
                    server.send(message.encode('utf-8'))
                    print(f"From: You")
                    print(f"Message: { plaintext }")
                    print(f"Encrypted Message: { ciphertext }\n")
                    sys.stdout.flush()

    server.close()