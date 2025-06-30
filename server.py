import asyncio
import websockets
import json
from presenceServer import PresenceServer
from group import Group
# from user import User

class User:
    def __init__(self,name,websocket):
        self.name = name
        self.websocket= websocket
        
    async def send_message(self, message):  
        await self.websocket.send(json.dumps(message))

class ChatServer:
    def __init__(self):
        self.users={}
        self.groups = {}
        self.presence=PresenceServer()
    
    async def register(self,websocket):
        await websocket.send(json.dumps({"type": "info", "message": "Enter your name:"}))
        username = await websocket.recv()
        user=None
        if username in self.users:
            user = self.users[username]
        else:
            user=User(username,websocket)
            self.users[username] = user
            print(f"[Server] Registered user: {username}")
        await user.send_message({"type": "info", "message": f"Welcome {username}!"})
        self.presence.user_connected(username)
        await self.broadcast_presence(username, "online")   
        return user
    
    def create_group(self,group_name,members):
        if group_name in self.groups:
            print(f"[Server] Group {group_name} already exists.")
            return False
        self.groups[group_name] = Group(group_name, members)
        print(f"[Server] Group {group_name} is created")
        return True
    
    async def route_message(self,packet,sender):
         recipient=packet["recipient"]
         if recipient in self.users:
            # print(self.users)
            print(f"[Server] Sending message from {sender.name} to {recipient}")
            # print(packet)
            await self.users[recipient].send_message(packet) 
         else:
            await sender.send_message({
                "type": "error",
                "message": f"User {recipient} is offline or not found."
            })
    
    async def route_group_message(self,packet,sender):
           group_name = packet["group"]
           if group_name not in self.groups:
                 await sender.send_message({
                     "type" :"error",
                     "message": "this group doesn't exist"
                 })
                 return    
           group=self.groups[group_name]
           if not group.is_member(sender.name):
              await sender.send_message({
                "type": "error",
                "message": f"You are not a member of group '{group_name}'"
              })
              return
           for user in group.get_members():
                if user!=sender.name and user in self.users:
                    print(f"[Server] Sending message to {sender.name} in {group_name}")
                    await self.users[user].send_message(packet) 
                            
    async def handle_client(self,websocket):
         user=await self.register(websocket)    
         print(f"[Server] User {user.name} connected.")     
         try:
             async for message in websocket:
                 print(message)
                 packet= json.loads(message)
                 packet["sender"]=user.name
                 if packet["type"] == "message":
                     await self.route_message(packet, sender=user)
                 elif packet["type"] == "group_message":
                     await self.route_group_message(packet,sender=user) 
                 elif packet["type"] == "create_group":
                      self.create_group(packet['group'],packet['members'])      
                 elif packet["type"] == "ack":
                     print(f"[Server] Acknowledgment from {user.name}: {packet['recipient']}")
                     if packet["recipient"] in self.users:
                        await self.users[packet["recipient"]].send_message(packet)
                 elif packet["type"] == "who_is_online":
                     users_list = self.presence.get_online_users()
                     await user.send_message({
                        "type": "info",
                        "message": f"Online users: {', '.join(users_list)}"
                     })
                 
         except websockets.exceptions.ConnectionClosed:
             print(f"[Server] Connection closed for user: {user.name}")
             self.presence.user_disconnected(user.name)
             await self.broadcast_presence(user.name, "offline")

    async def run(self,host='localhost', port=8765):
        async with websockets.serve(self.handle_client, host, port):
            print(f"[Server] Chat server started on ws://{host}:{port}")
            await asyncio.Future()

    async def broadcast_presence(self,username,status):
        packet={
            "type": "presence",
            "username": username,
            "status": status
        }
        for user in self.users.values():
            if user.name != username:
                await user.send_message(packet)

if __name__ == "__main__":
    server = ChatServer()
    asyncio.run(server.run())