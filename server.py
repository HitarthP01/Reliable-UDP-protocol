import socket
import threading
import random

# Define the server address and port
SERVER_IP = '142.58.211.109'
SERVER_PORT = 12000
BUFFER_SIZE = 1024
LOSS_PROBABILITY = 0.1
ERROR_PROBABILITY = 0.1

# Simulate packet loss
def should_drop_packet():
    return random.random() < LOSS_PROBABILITY

# Simulate bit error
def introduce_error(data):
    if random.random() < ERROR_PROBABILITY:
        error_index = random.randint(0, len(data)-1)
        data = data[:error_index] + bytes([data[error_index] ^ 0xFF]) + data[error_index+1:]
    return data

def handle_client(server_socket):
    while True:
        try:
            message, client_address = server_socket.recvfrom(BUFFER_SIZE)
            if should_drop_packet():
                print(f"Dropping packet from {client_address}")
                continue
            
            corrupted_message = introduce_error(message)
            
            try:
                decoded_message = corrupted_message.decode()
                print(f"Received message from {client_address}: {decoded_message}")
                
                ack_message = b"ACK:" + corrupted_message.split(b':')[0]
                server_socket.sendto(ack_message, client_address)
            except UnicodeDecodeError:
                print(f"Corrupted message from {client_address}, ignoring...")
        except Exception as e:
            print(f"Error: {e}")
            break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    handle_client(server_socket)

if __name__ == "__main__":
    main()
