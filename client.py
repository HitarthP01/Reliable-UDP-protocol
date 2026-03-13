import socket
import random
import time

# Define the server address and port
SERVER_IP = '142.58.211.109'
SERVER_PORT = 12000
BUFFER_SIZE = 1024
LOSS_PROBABILITY = 0.1
ERROR_PROBABILITY = 0.1
INITIAL_WINDOW_SIZE = 1
MAX_WINDOW_SIZE = 10
TIMEOUT = 1.0

# Simulate packet loss
def should_drop_packet():
    return random.random() < LOSS_PROBABILITY

# Simulate bit error
def introduce_error(data):
    if random.random() < ERROR_PROBABILITY:
        error_index = random.randint(0, len(data)-1)
        data = data[:error_index] + bytes([data[error_index] ^ 0xFF]) + data[error_index+1:]
    return data

# Unreliable data transfer: simulates sending with packet loss and bit errors
def udt_send(sock, address, message):
    if should_drop_packet():
        print(f"Dropping message: {message}")
    else:
        message = introduce_error(message)
        print(f"Sending message: {message}")
        sock.sendto(message, address)

# Reliable data transfer: ensures messages are sent reliably
def rdt_send(sock, address, data, seq_num):
    message = f"{seq_num}:{data}".encode()
    udt_send(sock, address, message)

# Receive function: handles acknowledgment and error checking
def rdt_receive(sock, expected_seq_num):
    try:
        ack_message, _ = sock.recvfrom(BUFFER_SIZE)
        decoded_message = ack_message.decode()
        print(f"Received ACK: {decoded_message}")
        if "ACK:" in decoded_message:
            ack_seq_num = int(decoded_message.split(":")[1])
            if ack_seq_num == expected_seq_num:
                return True
    except (UnicodeDecodeError, ValueError, IndexError) as e:
        print(f"Error decoding ACK: {e}")
    except socket.timeout:
        print("Timeout waiting for ACK")
    return False

def reliable_send(client_socket, server_address, data):
    base = 0
    next_seq_num = 0
    window = []
    window_size = INITIAL_WINDOW_SIZE

    while base < len(data):
        while next_seq_num < base + window_size and next_seq_num < len(data):
            rdt_send(client_socket, server_address, data[next_seq_num], next_seq_num)
            window.append(next_seq_num)
            next_seq_num += 1

        client_socket.settimeout(TIMEOUT)
        while window:
            if rdt_receive(client_socket, window[0]):
                base += 1
                window.pop(0)
                # Congestion control: Additive Increase
                if window_size < MAX_WINDOW_SIZE:
                    window_size += 1
            else:
                # Congestion control: Multiplicative Decrease
                window_size = max(1, window_size // 2)
                print(f"Resending window: {window}")
                for seq_num in window:
                    rdt_send(client_socket, server_address, data[seq_num], seq_num)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER_IP, SERVER_PORT)
    data = [f"Message {i}" for i in range(10)]

    reliable_send(client_socket, server_address, data)
    client_socket.close()

if __name__ == "__main__":
    main()
