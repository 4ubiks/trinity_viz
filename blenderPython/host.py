# updated on: 27 November 2024
# updated by: Jack Harris

import socket
import struct
import time
import threading

host = '192.168.0.166'
port = 65432

def client_handler(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            message = 15
            packed_message = struct.pack('!i', message)
            
            # Send message and check for any socket errors
            conn.sendall(packed_message)
            print(f"Sent message: {message}")
            
            # Wait for 5 seconds before sending the next packet
            time.sleep(0.5)
    except (ConnectionResetError, BrokenPipeError):
        print(f"Connection closed with {addr}")
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Server listening on {host}:{port}")
    
    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_handler, args=(conn, addr), daemon=True).start()
