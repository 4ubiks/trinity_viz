import bpy
import socket
import struct



def client():
    host = '127.0.0.1'
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

        # Apply the rotation to an object (for example, the active object)
        if bpy.context.active_object:
            bpy.context.active_object.rotation_euler[2] += rotation_angle  # Rotate on the Z axis
    c.close()

if __name__ == '__main__':
    client()    
