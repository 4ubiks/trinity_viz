# updated on: 27 November 2024
# updated by: Jack Harris

import bpy
import socket
import struct
import threading


def client():
    host = '192.168.0.166'
    port = 65432

    # Establish socket connection to the server
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c = socket.socket()
    c.connect((host, port))
    while True:
        data = c.recv(4)  # Receive 4 bytes (integer)
        unpacked_data = struct.unpack('!i', data)  # Unpack the integer

        # Get the rotation angle from the received data
        rotation_angle = unpacked_data[0]  # This is the received integer value (e.g., 15)

        print(f"Received rotation angle: {rotation_angle}")
            
        rotation_angle = (rotation_angle * 3.1415926535790) / 180

        bpy.app.timers.register(lambda: rotate(rotation_angle))
    c.close()
        
def rotate(rotation_angle):
    if bpy.context.active_object:
       bpy.context.active_object.rotation_euler[2] += rotation_angle
       print(f"rotating by: {rotation_angle}")
    else:
        print(f"no selected object")
    #print('hi')
    return None

if __name__ == '__main__':
    threading.Thread(target=client, daemon=True).start()

