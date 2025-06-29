import websockets
import json
class User:
    def __init__(self,name,websocket):
        self.name = name
        self.websocket= websocket
        
    async def send_message(self, message):
        print(f"[Server] Sending: {message}")
        await self.websocket.send(json.dumps(message))

    