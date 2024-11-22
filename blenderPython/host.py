import socket

# Host server setup
host = '127.0.0.1'  # Localhost
port = 65432        # Port to bind to

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Server listening on {host}:{port}...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        # Send some data to Blender
        message = "Hello from the server!"
        conn.sendall(message.encode())
