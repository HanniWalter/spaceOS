#from src.gameobjects.Spaceship import Spaceship
import src.gameobjects.Game_Object as Game_Object
import src.gameobjects.Player as Player
import src.gameobjects.Spaceship as Spaceship
import src.util.docker_manager as docker_manager

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
        return f"Spaceship {len(self.game_ref.objects)}"
    
    def set_name(self, name,new_spaceship=False):
        if new_spaceship:
            if name == "":
                self.spaceship_config["name"] = self.create_next_name()
            else:
                self.spaceship_config["name"] = name
        else:
            if name == "":
                self.spaceship_modification_config["name"] = self.create_next_name()
            else:
                self.spaceship_modification_config["name"] = name

    def get_oss(self):
        return [os.name for os in docker_manager.oss]
    
    def set_os(self, os, new_spaceship=False):
        if new_spaceship:
            self.spaceship_config["os"] = os
        else:
            self.spaceship_modification_config["os"] = os


    def prepare_config(self):
        self.spaceship_config = {}
        self.spaceship_config["name"] = self.create_next_name()
        self.spaceship_config["os"] = docker_manager.oss[0].name

    def prepare_modification_config(self, spaceship_id):
        spaceship = self.player.get_spaceship(spaceship_id)
        self.spaceship_modification_config = {}
        self.spaceship_modification_config["name"] = spaceship.name
        self.spaceship_modification_config["id"] = spaceship.id
        self.spaceship_modification_config["os"] = spaceship.operating_system.name

    def build_spaceship(self):
        spaceship = Spaceship.Spaceship.new(self.game_ref,self.spaceship_config["name"], "test")
        self.player.spaceships.append(spaceship)
        return spaceship

    def modify_spaceship(self):
        spaceship_id = self.spaceship_modification_config["id"]
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