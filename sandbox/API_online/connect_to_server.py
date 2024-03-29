import socket

def connect_to_server(host, port):
    with socket.create_connection((host, port)) as sock:
        sock.sendall("Hello, server!".encode())
        response = sock.recv(1024)
        print(f"Received: {response.decode()}")

if __name__ == '__main__':
    connect_to_server('localhost', 5001)
