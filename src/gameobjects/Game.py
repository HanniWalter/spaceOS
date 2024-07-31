
import threading
import time
import json
import glob
import numpy as np
import importlib
if __name__ == "__main__":
    import sys
    sys.path.append(".")

# load own package
from src.util import docker_manager
import src.gameobjects.Player as Player
import src.gameobjects.Game_Object as Game_Object
import src.gameobjects.Spaceship as Spaceship
import src.gameobjects.Component as Component


def isSubclass(obj, cls):
    if obj == cls:
        return True
    for base in obj.__bases__:
        if isSubclass(base, cls):
            return True
    return False


allclasses = {}
for file in glob.glob("src/gameobjects/*.py"):
    if file == "src/gameobjects/Game.py":
        continue
    if file == "src/gameobjects/__init__.py":
        continue
    module = importlib.import_module(
        file.replace("/", ".").replace("\\", ".")[:-3])
    # get classes from module only include subclasses of Game_Object
    for name, obj in module.__dict__.items():
        # check is class
        if isinstance(obj, type):
            if isSubclass(obj, Game_Object.Game_Object):
                allclasses[name] = obj
            #


class Game:
    def __init__(self):
        self.initiated = False
        self.time = -1
        self.lock = threading.Lock()
        self.objectcount = 0
        self.objects = {}
        self.stopped = True
        self.start()

    def new_game():
        ret = Game()
        ret.players = []
        ret.initiated = True
        ret.continue_game()

        return ret

    def continue_game(self):
        self.stopped = False

    def stop_game(self):
        self.stopped = True

    def load_game(savegame):
        data = savegame["data"]
        r = from_dict(data, None)
        r.continue_game()
        return r

    def saveGameData(self, savegame_name):
        ret = {}
        ret["data"] = to_dict(self, forced=True)
        ret["time"] = time.time()
        ret["savegame_name"] = savegame_name
        return ret

    def update(self, delta: float):
        self.time += delta
        for player in self.players:
            player.update(delta)

    def loop(self):
        running_time = -2
        while True:
            with self.lock:
                if self.initiated:
                    if self.stopped:
                        print("stopped game")
                        break
                    if running_time == -2:
                        running_time = time.time()
                    else:
                        time_ = time.time()
                        diff = time_ - running_time
                        running_time = time_
                        self.update(diff)

            time.sleep(0)

    def start(self):
        threading.Thread(target=self.loop).start()

    def test_data(self):
        ships = []
        for x in range(0, 5):
            ship = Spaceship.Spaceship.new(
                game_ref=self, name="Spaceship "+str(x), operating_system="test")
            self.players[0].spaceships.append(ship)

            ships.append(ship)
            clock = Component.Clock.new(parent=ship, game_ref=self)
            teleporter = Component.Teleporter.new(parent=ship, game_ref=self)

        ships[0].location = np.array([-1000, -1000, 0])
        ships[1].location = np.array([1000, -1000, 0])
        ships[2].location = np.array([-1000, 1000, 0])
        ships[3].location = np.array([1000, 1000, 0])

# for what is forced?
# its for saving the top level gameobject, elsewise Game would only be saved as a reference


def to_dict(obj, forced=False):
    if isinstance(obj, Game):
        if forced:
            d = {}
            d["type"] = "Game"
            for key in obj.__dict__:
                if key == "initiated":
                    continue
                if key == "lock":
                    continue
                if key == "objects":
                    d[key] = [to_dict(obj, forced=True)
                              for obj in obj.__dict__[key].values()]
                    continue
                d[key] = to_dict(obj.__dict__[key])
            return d
        else:
            d = {}
            d["type"] = "game_ref"
            return d

    if isinstance(obj, Game_Object.Game_Object):
        if forced:
            d = {}
            d["type"] = "Game_Object"
            d["class"] = obj.__class__.__name__
            d["value"] = {key: to_dict(obj.__dict__[key])
                          for key in obj.__dict__}
            return d
        d = {}
        d["type"] = "ref"
        d["id"] = obj.id
        d["class"] = obj.__class__.__name__
        return d
    if isinstance(obj, docker_manager.Operating_System):
        d = {}
        d["type"] = "Operating_System"
        d["value"] = obj.path
        return d
    if isinstance(obj, int):
        d = {}
        d["type"] = "int"
        d["value"] = obj
        return d
    if isinstance(obj, float):
        d = {}
        d["type"] = "float"
        d["value"] = obj
        return d
    if isinstance(obj, str):
        d = {}
        d["type"] = "str"
        d["value"] = obj
        return d
    if isinstance(obj, list):
        d = {}
        d["type"] = "list"
        d["value"] = [to_dict(item) for item in obj]
        return d
    if isinstance(obj, np.ndarray):
        d = {}
        d["type"] = "ndarray"
        d["value"] = obj.tolist()
        return d
    if isinstance(obj, dict):
        d = {}
        d["type"] = "dict"
        d["value"] = [[to_dict(key), to_dict(value)]
                      for key, value in obj.items()]
        return d

    print("unknown type:", type(obj), obj)
    assert False, "unknown type:" + type(obj) + "" + str(obj)

# you may ask what is no_ref for?
# it is for the loading of the game; first all objects are created without references
# then all objects are created with references with only_ref on


def from_dict(d, game_ref, no_ref=False, only_ref=False):
    assert type(d) == dict, "d is not a dict"
    assert "type" in d, "no type in dict"
    if d["type"] == "Game":
        r = Game()
        for obj in d["objects"]:
            r.objects[obj["value"]["id"]["value"]
                      ] = from_dict(obj, r, no_ref=True)
        for obj in d["objects"]:
            r.objects[obj["value"]["id"]["value"]
                      ] = from_dict(obj, r, only_ref=True)

        for key in d:
            if key == "type":
                continue
            if key == "objects":
                continue
            r.__dict__[key] = from_dict(d[key], r)
        return r
    if d["type"] == "game_ref":
        return game_ref
    if d["type"] == "Game_Object":
        if only_ref:
            r = game_ref.objects[d["value"]["id"]["value"]]
        else:
            cls = d["class"]
            # error global[cls] returns the module not the class
            r = allclasses[cls](game_ref=game_ref, silent=True)
        for key in d["value"]:
            r.__dict__[key] = from_dict(
                d["value"][key], game_ref, no_ref=no_ref, only_ref=only_ref)
        return r
    if d["type"] == "ref":
        if no_ref:
            return None
        return game_ref.objects[d["id"]]

    if d["type"] == "int":
        return int(d["value"])
    if d["type"] == "float":
        return float(d["value"])
    if d["type"] == "str":
        return str(d["value"])
    if d["type"] == "list":
        return [from_dict(item, game_ref, no_ref) for item in d["value"]]
    if d["type"] == "Operating_System":
        return docker_manager.get_os_path(d["value"])
    if d["type"] == "ndarray":
        return np.array(d["value"])
    if d["type"] == "dict":
        return {from_dict(key, game_ref, no_ref, only_ref): from_dict(value, game_ref, no_ref, only_ref) for [key, value] in d["value"]}
    print(d["type"])

    assert False, "something went wrong"


if __name__ == "__main__":
    import src.gameobjects.Spaceship as Spaceship

    game = Game.new_game()
    # game.player.spaceships.append(Spaceship(game_ref=game, silent=False))
    d = to_dict(game, forced=True)
    game.running = False
    game.stopped = True
    game = from_dict(d, None)
    game.continue_game()
