import asyncio
import json
import websockets

class Group:
    def __init__(self,name,members):
        self.name = name
        self.users = set(members)

        