import glob
import json
import random

### Game logic ###
def getSavegames():
    savegames = []
    for savegame in glob.glob("resources/savegames/*"):
        savegames.append(savegame)
    return savegames

class Spaceship:
    def __init__(self):
        if not game.initiated:
            return
        self.name = "spaceship1"
        self.hull = 100
        self.shield = 100
        self.docker_image = "test"
        while True:
            self.id = random.randint(0,1000000)
            if not self.id in [spaceship.id for spaceship in game.player.spaceships]:
                break

    def to_dict(self):
        return {
            "name": self.name,
            "hull": self.hull,
            "shield": self.shield,
            "docker_image": self.docker_image,
            "id": self.id  
        }

    def from_dict(spaceship_dict):
        spaceship = Spaceship()
        spaceship.name = spaceship_dict["name"]
        spaceship.hull = spaceship_dict["hull"]
        spaceship.shield = spaceship_dict["shield"]
        spaceship.docker_image = spaceship_dict["docker_image"]
        spaceship.id = int(spaceship_dict["id"])
        return spaceship
    
class Player:
    def __init__(self):
        self.name = "player1"
        self.spaceships = []
        self.money = 1000
    
    def to_dict(self):
        return {
            "name": self.name,
            "spaceships": [spaceship.to_dict() for spaceship in self.spaceships],
            "money": self.money
        }
    
    def from_dict(player_dict):
        player = Player()
        player.name = player_dict["name"]
        player.spaceships = [Spaceship.from_dict(spaceship_dict) for spaceship_dict in player_dict["spaceships"]]
        player.money = player_dict["money"]
        return player

class Game:
    def __init__(self):
        self.initiated = False

    def new_game(self):
        self.player = Player()
        self.initiated = True

    def load_game(savegame_name):
        #load game from file
        with open("resources/savegames/"+savegame_name, "r") as savegame:
            game.from_dict(json.loads(savegame.read()))

    def save_game(self, savegame_name = "savegame"):
        #save game to file
        with open("resources/savegames/"+savegame_name, "w") as savegame:
            savegame.write(json.dumps(self.to_dict()))


    def to_dict(self):
        if self.initiated:
            return {
                "initiated": self.initiated,
                "player": self.player.to_dict()
            }
        else:
            return {
                "initiated": self.initiated
            }

    def from_dict(self,game_dict):
        self.player = Player.from_dict(game_dict["player"])
        self.initiated = game_dict["initiated"]

game = Game()