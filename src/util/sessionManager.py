
class SessionManager():
    def __init__(self):
        self.sessions = []


class Session():
    def __init__(self, Player, permission_level="player"):
        self.player = Player
        #hash player name for id
        self.session_id = hash(Player.name)


        sessions.append(self)


    