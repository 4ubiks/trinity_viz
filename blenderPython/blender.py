import asyncio
import websockets
import json

# WebSocket Server
async def handler(websocket, path):
    print("Client connected")
    try:
        while True:
            message = await websocket.recv()  # Receive message from Blender
            print(f"Received message: {message}")
            
            # Process the message (Example: parsing and sending back location data)
            data = json.loads(message)
            response = {
                "message": "Data received",
                "location": data.get("location", None)
            }
            await websocket.send(json.dumps(response))  # Send back to Blender
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

# Start WebSocket server
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run server forever

# Run the WebSocket server
asyncio.run(main())
