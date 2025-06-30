import asyncio
import json
import websockets

class Group:
    def __init__(self,name,members=None):
        self.name = name
        self.users = set(members or [])
        self.admins=set()
    
    def add_user(self, user):
        self.users.add(user)
    
    def remove_user(self, user):
        self.users.discard(user)    
    
    def is_member(self, user):
        return user in self.users
    
    def get_members(self):
        return list(self.users)    