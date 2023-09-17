import asyncio
import websockets

connected = set()


async def server(websocket, path):
    connected.add(websocket)
    try:
        # 接続の状態を確認
        if websocket.open:
            print(f"WebSocket connection is open: {websocket.remote_address}")
        else:
            print(
                f"WebSocket connection is closed: {websocket.remote_address}")

        async for message in websocket:
            print(f"Received message: {message}")
            for conn in connected:
                print("New message loop iteration")
                try:
                    print(f"Trying to send message to a client: {message}")
                    await conn.send(message)
                    print(f"Sent message to client: {message}")
                except Exception as e:
                    print(f"Error while sending: {e}")
                    print(f"Connection state: {conn.state}")

        # 接続の状態を再度確認
        if websocket.open:
            print(
                f"WebSocket connection remains open: {websocket.remote_address}")
        else:
            print(
                f"WebSocket connection was closed: {websocket.remote_address}")

    except websockets.ConnectionClosed as e:
        print(f"WebSocket connection was closed with code: {e.code}")

    finally:
        connected.remove(websocket)

start_server = websockets.serve(server, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
