import asyncio
import websockets
import json

class Client:
    def __init__(self,uri='ws://localhost:8765'):
        self.uri=uri
        self.username = None
    
    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        await self.handle_initial()
        await asyncio.gather(
                self.receive_loop(),
                self.send_loop()
            )
        
    async def handle_initial(self):
        msg= await self.websocket.recv()    
        self.username = await asyncio.get_event_loop().run_in_executor(None, input, "Enter your name: ")
        await self.websocket.send(self.username)
        welcome = await self.websocket.recv()
        print(json.loads(welcome)["message"])      
        print(f"[Client] Connected as {self.username}")

    async def send_loop(self):
        loop = asyncio.get_event_loop()
        while True:
            command = await loop.run_in_executor(None, input, "Send to user or type '/group ")
            if command == "/group":
                group = await loop.run_in_executor(None, input,"Group name: ")
                content = await loop.run_in_executor(None, input,"Message: ")
                packet = {
                    "type": "group_message",
                    "group": group,
                    "content": content
                }
                await self.websocket.send(json.dumps(packet))
            
            elif command == "/create":
                group =await loop.run_in_executor(None, input,"New group name: ")
                members = await loop.run_in_executor(None, input,"Enter members (comma separated): ")
                members=members.split(",")
                members = [m.strip() for m in members]
                packet = {
                    "type": "create_group",
                    "group": group,
                    "members": members
                }
                await self.websocket.send(json.dumps(packet))
            elif command=="/online":
                await self.websocket.send(json.dumps({
                "type": "who_is_online"
                }))
                continue
            else:
                recipient = command
                content = await loop.run_in_executor(None, input, "Message: ")
                packet = {
                    "type": "message",
                    "recipient": recipient,
                    "content": content
                }
                await self.websocket.send(json.dumps(packet))
            
            # if recipient == "/online":
            #   await self.websocket.send(json.dumps({
            #     "type": "who_is_online"
            #     }))
            #   continue
            # packet = {
            #     "type": "message",
            #     "recipient": recipient,
            #     "content": content
            # }
            # await self.websocket.send(json.dumps(packet))   
        
    async def receive_loop(self):
        try:
            while True:
                msg = await self.websocket.recv()
                data = json.loads(msg)

                if data["type"] == "message":
                    print(f"\n[DM] {data['sender']} ➝ {self.username}: {data['content']}")
                    await self.websocket.send(json.dumps({
                        "type": "ack",
                        "recipient": data["sender"],
                        "content": f"ACK: received '{data['content']}'"
                    }))

                elif data["type"] == "ack":
                    print(f"\n[ACK] {data['sender']} ➝ {self.username}: {data['content']}")
                elif data["type"] == "info":
                    print(f"[INFO] {data['message']}")
                elif data["type"] == "error":
                    print(f"[ERROR] {data['message']}")
                elif data["type"] == "presence":
                    print(f"[Presence] {data['username']} is now {data['status']}")
                elif data["type"] == "group_message":
                    print(f"\n[Group:{data['group']}] {data['sender']}: {data['content']}")  
                          
        except websockets.exceptions.ConnectionClosed as e:
            print(f"[Client] Connection closed: {e}")

if __name__ == "__main__":
    client = Client()
    asyncio.run(client.connect())