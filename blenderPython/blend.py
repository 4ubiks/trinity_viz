# updated on: 27 November 2024
# updated by: Jack Harris

# this is what runs inside blender. 
# do not try to run this on a host machine, it won't work. 

import bpy
import socket
import struct
import threading


def client():
    host = '192.168.0.166'                    # ip address of a test device, this can change
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
            
        # convert to degrees 
        rotation_angle = (rotation_angle * 3.1415926535790) / 180

        # calls the rotation function, uses `lambda` as a wrapper because we are passing a value
        bpy.app.timers.register(lambda: rotate(rotation_angle))
    c.close()
        
def rotate(rotation_angle):
    # check there is an active or target object
    if bpy.context.active_object:
       bpy.context.active_object.rotation_euler[2] += rotation_angle
       print(f"rotating by: {rotation_angle}")
    else:
        print(f"no selected object")
    return None

if __name__ == '__main__':
    # runs the process on a specific thread to prevent blender from crashing
    threading.Thread(target=client, daemon=True).start()

