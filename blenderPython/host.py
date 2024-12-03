# updated on: 27 November 2024
# updated by: Jack Harris

# this is to run on the ground station, retrieving data from the rocket. 

import socket
import struct
import time
import threading
import random

host = '127.0.0.1'
port = 65432

def client_handler(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            message = random.randint(15, 30)
            packed_message = struct.pack('!i', message)
            
            # Send message and check for any socket errors
            conn.sendall(packed_message)
            print(f"Rotational Value: {message} degrees")
            
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
