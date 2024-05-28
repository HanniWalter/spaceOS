#from src.gameobjects.Spaceship import Spaceship
import src.gameobjects.Game_Object as Game_Object
import src.gameobjects.Player as Player
import src.gameobjects.Spaceship as Spaceship

class Spaceship_Factory(Game_Object.Game_Object):
    def __init__(self, game_ref=None, silent=False):
        super().__init__(game_ref, silent)

    def new(player, game_ref):
        r = Spaceship_Factory(game_ref=game_ref, silent=False)
        r.player = player
        r.spaceship_config = {}
        r.spaceship_modification_config = {}
        return r

    def build_spaceship(self):
        spaceship = Spaceship.Spaceship.build_spaceship(self.spaceship_config)
        self.player.spaceships.append(spaceship)
        return spaceship

    def modify_spaceship(self, spaceship_id):
        spaceship = self.player.get_spaceship(spaceship_id)
        spaceship.modify(self.spaceship_modification_config)
        return spaceship
    
    def change_name(self, new_name):
        pass
     