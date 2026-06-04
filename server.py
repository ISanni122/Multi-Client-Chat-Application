import socket
import threading
import ssl

#  Server configuration
HOST = "localhost"   # localhost – change it later justin
PORT = 55556         # port the server listens on

# Lists that track every connected client
clients  = []   # socket objects
usernames = []  # matching display names


#  Broadcast a message to ALL connected clients
def broadcast(message):
    # Send a message to every client in the list.
    for client in clients:
        client.send(message)


#  Handle one client 
def handle_client(client):
    ##  Continuously receive messages from a single client. 
    #  If the client sends 'bye' or disconnects, remove them and notify everyone else.

    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            # Client wants to leave 
            if message.lower().strip() == "bye":
                index = clients.index(client)
                username = usernames[index]

                # Clean up tracking lists
                clients.remove(client)
                usernames.remove(username)
                client.close()

                broadcast(f"{username} has left the chat.\n".encode("utf-8"))
                print(f"[SERVER] {username} disconnected.")
                break   # exit the loop – thread ends naturally

            # Normal message: forward to everyone 
            else:
                broadcast(message.encode("utf-8"))

        except:
            # Handles sudden disconnects like closing the terminal window 
            try:
                index = clients.index(client)
                username = usernames[index]
                clients.remove(client)
                usernames.remove(username)
                client.close()
                broadcast(f"{username} lost connection.\n".encode("utf-8"))
                print(f"[SERVER] {username} lost connection.")
            except ValueError:
                pass    # client was already removed
            break


#  Main: set up the socket and accept clients
def start_server():
    ## Create the server socket and enter the connection-accept loop.

    # Create the SSL context and load the certificate and key
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    raw_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # avoids "address already in use" on restart
    raw_server.bind((HOST, PORT))
    raw_server.listen(5)    # queue up to 5 pending connections

    # Wrap the raw server socket with SSL
    server = context.wrap_socket(raw_server, server_side=True)
    print(f"[SERVER] SSL enabled. Listening on {HOST}:{PORT} ...")

    while True:
        # Block here until a new client connects
        client, address = server.accept()
        print(f"[SERVER] Secure connection from {address}")

        # Ask the client to send their username right away
        client.send("USERNAME".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")

        # Register the new client
        clients.append(client)
        usernames.append(username)
        print(f"[SERVER] Username registered: {username}")

        # Tell everyone a new person joined
        broadcast(f"{username} joined the chat!\n".encode("utf-8"))
        client.send("Connected to the server!\n".encode("utf-8"))

        # Spin up so this client doesn't block others
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True    # thread closes automatically if main program exits
        thread.start()


#  Entry point
if __name__ == "__main__":
    start_server()