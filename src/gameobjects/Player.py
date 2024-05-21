from src.gameobjects.Game_Object import Game_Object

class Player(Game_Object):
    def __init__(self,game_ref = None, silent = False):
        super().__init__(game_ref= game_ref,silent=silent)
        self.name = "player1"
        self.spaceships = []
        self.money = 1000

    def get_spaceship(self, spaceship_id):
        for spaceship in self.spaceships:
            if int(spaceship.id) == int(spaceship_id):
                return spaceship
        return None
    
    def update(self, delta: float):
        for spaceship in self.spaceships:
            spaceship.update(delta)

