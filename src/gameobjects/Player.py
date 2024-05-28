
import src.gameobjects.Game_Object as Game_Object
import src.gameobjects.Spaceship_Factory as Spaceship_Factory

class Player(Game_Object.Game_Object):
    def __init__(self, game_ref=None, silent=False):
        super().__init__(game_ref=game_ref, silent=silent)
        
    def new(game_ref, name: str):
        r = Player(game_ref=game_ref, silent=False)
        r.name = name
        r.spaceships = []
        r.money = 1000
        r.spaceship_factory = Spaceship_Factory.Spaceship_Factory.new(r, game_ref)
        return r

    def get_spaceship(self, spaceship_id):
        for spaceship in self.spaceships:
            if int(spaceship.id) == int(spaceship_id):
                return spaceship
        return None

    def update(self, delta: float):
        for spaceship in self.spaceships:
            spaceship.update(delta)

