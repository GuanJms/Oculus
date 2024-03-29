import requests
import socket

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return "Unable to determine public IP."

def check_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', port))
        sock.listen(1)
        return True

if __name__ == '__main__':
    public_ip = get_public_ip()
    server_port = 5002  # Change this to your server's port
    port_open = check_port_open(server_port)

    print(f"Public IP: {public_ip}")
    print(f"Server Listening Port: {server_port}")
    if port_open:
        print(f"Port {server_port} is ready to accept connections.")
    else:
        print(f"Port {server_port} is not open or is already in use.")
