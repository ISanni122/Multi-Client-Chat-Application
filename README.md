# Multi-Client-Chat-Application
Project Description


The proposed project is a multi-client chat application programmed in Python. The project will support multiple clients connecting to a locally hosted server, allowing for real-time communication amongst the connecting clients. The TCP protocol will be used to ensure clients are able to reliably send and receive messages in a group chat. To facilitate private communication between clients, the application will utilize Python’s SSL module to implement TLS encryption. To support multiple clients connecting to the server, the application will use Python’s threading module.


Features


Core features of the project will include:

A server capable of handling multiple users connecting simultaneously and allowing clients to send messages concurrently in real-time
A client username registration system, allowing users to identify each other easily
TLS encryption preventing external actors from intercepting messages and reading the contents
Chat history being saved to a log file local to the server
Error handling for connectivity issues or invalid inputs from clients such as a blank space username
