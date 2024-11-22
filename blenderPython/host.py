import socket
import struct

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
        # Send the integer as raw bytes
        message = 15
        packed_message = struct.pack('!i', message)  # Pack integer 'message' to bytes (big-endian)
        conn.sendall(packed_message)  # Send the raw bytes
