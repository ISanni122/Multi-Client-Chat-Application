import socket
from threading import Thread
import ssl
import os

class Client:

    def __init__(self, HOST, PORT):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Create SSL context for the client
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        
        # Load the server's cert to verify it (since it's self-signed)
        context.load_verify_locations("server.crt")

        self.socket = context.wrap_socket(raw_socket, server_hostname=HOST)
        self.socket.connect((HOST, PORT))
        self.name = input("Enter your name: ")

        self.talk_to_server()

    def talk_to_server(self):
        prompt = self.socket.recv(1024).decode()
        if prompt == "USERNAME":
            self.socket.send(self.name.encode())

        Thread(target=self.receive_message, daemon=True).start()
        self.send_message()

    def send_message(self):
        while True:
            client_input = input("")
            client_message = self.name + ": " + client_input
            self.socket.send(client_message.encode())

    def receive_message(self):
        while True:
            server_message = self.socket.recv(1024).decode()
            if not server_message.strip():
                os._exit(0)
            print(server_message)

if __name__ == "__main__":
    Client('localhost', 55556)