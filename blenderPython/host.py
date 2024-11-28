import socket
import struct
import threading
import time

host = '192.168.0.166'
port = 65432

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            message = 15
            packed_message = struct.pack('!i', message)
            conn.sendall(packed_message)
            # Pause, but don't block Blender entirely, maybe use configurable wait
            time.sleep(5)
    except ConnectionResetError:
        print("Connection closed.")
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Server listening on {host}:{port}...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
