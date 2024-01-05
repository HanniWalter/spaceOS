import glob
import json
import random
import docker_manager
import threading
import time

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
        self.operating_system = docker_manager.get_os_name("test")
        self.started = False
        while True:
            self.id = random.randint(0, 1_000_000)
            if not self.id in [spaceship.id for spaceship in game.player.spaceships]:
                break

    def to_dict(self):

        return {
            "name": self.name,
            "hull": self.hull,
            "shield": self.shield,
            "operating_system": self.operating_system.path,
            "id": self.id,
            "started": self.started
        }

    def from_dict(spaceship_dict):
        if not "started" in spaceship_dict:
            spaceship_dict["started"] = False
        spaceship = Spaceship()
        spaceship.name = spaceship_dict["name"]
        spaceship.hull = spaceship_dict["hull"]
        spaceship.shield = spaceship_dict["shield"]
        spaceship.operating_system = docker_manager.get_os_name(spaceship_dict["operating_system"])
        spaceship.id = int(spaceship_dict["id"])
        if spaceship_dict["started"]:
            spaceship.start()
        spaceship.started = spaceship_dict["started"]
        return spaceship

    def start(self):
        if self.started:
            return
        self.started = True
        os = self.operating_system
        self.container = os.run()

    def is_running(self):
        if not self.started:
            return False
        if not self.container:
            print("Container not found")
            return False
        return docker_manager.is_container_running(self.container)

    def attach_console(self):
        if not self.started:
            return
        if not self.container:
            print("Container not found")
            return
        docker_manager.attach_console(self.container)

    def update_spaceship(self, delta: float):
        if not self.started:
            return
        assert self.container, "Container not found"
        sensor = {
            "update_time": game.time,
        }

        control = docker_manager.read_from_container(self.container, dir="/ship/", filename="control")
        docker_manager.write_to_container(container=self.container,content=json.dumps(sensor),  dir="/ship/", filename="sensor")
        print(control)

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
        player.spaceships = [Spaceship.from_dict(
            spaceship_dict) for spaceship_dict in player_dict["spaceships"]]
        player.money = player_dict["money"]
        return player

    def get_spaceship(self, spaceship_id):
        for spaceship in self.spaceships:
            if int(spaceship.id) == int(spaceship_id):
                return spaceship
        return None
    
    def update(self, delta: float):
        for spaceship in self.spaceships:
            spaceship.update_spaceship(delta)

class Game:
    def __init__(self):
        self.initiated = False
        self.time = 0
        self.lock = threading.Lock()

    def new_game(self):
        self.player = Player()
        self.initiated = True

    def load_game(self,savegame_name):
        # load game from file
        with open("resources/savegames/"+savegame_name, "r") as savegame:
            self.from_dict(json.loads(savegame.read()))

    def save_game(self, savegame_name="savegame"):
        # save game to file
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

    def from_dict(self, game_dict):
        self.player = Player.from_dict(game_dict["player"])
        self.initiated = game_dict["initiated"]

    def update(self, delta: float):
        self.time += delta
        self.player.update(delta)
        print(1/delta, self.time)


game = Game()

def game_loop():
    running_time = -1
    while True:
        with game.lock:
            if game.initiated:
                if running_time == -1:
                    running_time = time.time()
                else:
                    time_ = time.time()
                    diff = time_ - running_time
                    running_time = time_
                    game.update(diff)

        time.sleep(1)

threading.Thread(target=game_loop).start()