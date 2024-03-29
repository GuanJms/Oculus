import socket
import threading


def handle_client_connection(client_socket):
    try:
        request = client_socket.recv(1024)
        print(f"Received request: {request.decode()}")
        client_socket.send("Response from server: your request was processed".encode())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


def start_server(host='0.0.0.0', port=5001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            client_sock, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
            client_handler.start()


if __name__ == '__main__':
    start_server()
