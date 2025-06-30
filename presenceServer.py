class PresenceServer:
    def __init__(self):
        self.online_users=set()
        
    def user_connected(self,username):
        self.online_users.add(username)
        print(f"[Server] User {username} connected. Online users: {self.online_users}")
    def user_disconnected(self,username):
        if username in self.online_users:
            self.online_users.remove(username)
            print(f"[Server] User {username} disconnected. Online users: {self.online_users}")
        else:
            print(f"[Server] User {username} not found in online users.")    
    def get_online_users(self):
        return list(self.online_users)