import socket
import threading

clients = {}

def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            decoded_data = data.decode('utf-8')
            print(f"Received from {client_address}: {decoded_data}")
            
            # Broadcast the received data to all clients
            broadcast(f"Broadcast from {client_address}: {decoded_data}")
            
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
        
    finally:
        print(f"Connection with {client_address} closed.")
        del clients[client_address]
        client_socket.close()

def broadcast(message):
    for address, socket in clients.items():
        try:
            socket.send(bytes(message, 'utf-8'))
        except Exception as e:
            print(f"Error broadcasting to {address}: {e}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1234))
    server.listen(5)
    
    print("Server listening on port...")
    
    try:
        while True:
            client_socket, client_address = server.accept()
            print(f"Connection established with {client_address}")
            
            # Send the client its own address immediately after connection
            client_socket.send(bytes(f"Echo:{client_address}", 'utf-8'))
            
            print(f"Sending the client its address ")
            
            clients[client_address] = client_socket
            
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
            
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()