import socket
import struct
import bpy
import threading

def receive_data():
    host = '192.168.0.166'  # Host machine IP
    port = 65432
    
    try:
        s= socket.socket()
        s.connect((host, port))
        print("Connected to server")

        while True:
            data = s.recv(4)  # Read exactly 4 bytes (for an integer)
            if not data:
                break
                
            unpacked_data = struct.unpack('!i', data)
            print(f"Received: {unpacked_data[0]}")
                
            rotation_angle = unpacked_data[0]
                
            print(f"received: {rotation_angle}")
                
            rotation_angle = (rotation_angle * 3.1415926535) / 180
                
            if bpy.context.active_object:
                bpy.context.active_object.rotation_euler[2] += rotation_angle  # Rotate on the Z axis
 
            # Use Blender-friendly logic, running on its internal thread:
            bpy.app.timers.register(lambda: update_blender_scene(message), first_interval=0.1)
    except Exception as e:
        print(f"Connection error: {e}")

def update_blender_scene(message):
    # Here we manipulate Blender objects based on incoming data.
    # Replace with your specific Blender operations:
    print(f"Processing data in Blender: {message}")
    # Example: print operation to confirm non-freezing
    return None  # Returning None lets the timer auto-stop.

# Start server-client in background without locking Blender UI
threading.Thread(target=receive_data, daemon=True).start()
