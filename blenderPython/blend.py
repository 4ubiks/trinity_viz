import socket

# Server connection settings
host = '172.22.44.125'
port = 65432

# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    data = s.recv(1024)  # Receive data from server
    print(f"Received from server: {data.decode()}")
