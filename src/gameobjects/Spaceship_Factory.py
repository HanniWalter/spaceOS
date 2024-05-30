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
        r.prepare_config()
        return r

    def create_next_name(self):
        return "Spaceship " + str(len(self.player.spaceships))

    def prepare_config(self):
        self.spaceship_config = {}
        self.spaceship_config["name"] = self.create_next_name()

    def prepare_modification_config(self, spaceship_id):
        spaceship = self.player.get_spaceship(spaceship_id)
        self.spaceship_modification_config = {}
        self.spaceship_modification_config["name"] = spaceship.name
        self.spaceship_modification_config["id"] = spaceship.id

    def build_spaceship(self):
        spaceship = Spaceship.Spaceship.build_spaceship(self.spaceship_config)
        self.player.spaceships.append(spaceship)
        return spaceship

    def modify_spaceship(self, spaceship_id):
        spaceship = self.player.get_spaceship(spaceship_id)
        spaceship.modify(self.spaceship_modification_config)
        return spaceship
     
    def clone_spaceship(self):
        config = self.spaceship_modification_config
        config["id"] = None
        spaceship = Spaceship.Spaceship.build_spaceship(self.spaceship_modification_config)
        self.player.spaceships.append(spaceship)
        return spaceship
    
    def apply_ship_to_template(self):
        self.spaceship_config = self.spaceship_modification_config