import random


class SessionManager():
    def __init__(self):
        self.sessions = {}
        self.nextId = 0
        self.admin_password = random.randint(0, 2**32)

    def new_session(self, Player, permission_level="player"):
        id = self.nextId
        self.nextId += 1
        d = {"player": Player, "permission_level": permission_level, "id": id}

        self.sessions[id] = d
        return id

    def check_admin(self, session_id):
        if session_id not in self.sessions:
            return False
        return self.sessions[session_id]["permission_level"] == "admin"

    def get_player(self, session_id):
        if session_id not in self.sessions:
            return None
        return self.sessions[session_id]["player"]
