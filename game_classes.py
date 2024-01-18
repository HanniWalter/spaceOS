import glob
import json
import random
import docker_manager
import threading
import time
import numpy as np
import toml

### Game logic ###


def getSavegames():
    savegames = []
    for savegame in glob.glob("resources/savegames/*"):
        savegames.append(savegame)
    return savegames

class Game_Object:
    def __init__(self, game_ref = None, silent = False):
        if silent:
            return
        assert game_ref, "game_ref is needed in nonsilent mode"
        self.id = game_ref.objectcount
        game_ref.objectcount += 1
        game_ref.objects[self.id] = self

        self.game_ref = game_ref

    #todo:
    #add here a lot of work for example it is not possible to change the os
    def apply_template(self, template):
        for key in template:
            if key in self.__dict__:
                if type(self.__dict__[key]) != type(template[key]):
                    return
            self.__dict__[key] = template[key]

class Thruster(Game_Object):
    def __init__(self,game_ref = None, silent=False):
        super().__init__(game_ref,silent)
    
    def new(game_ref, relative_position, direction, power):
        r = Thruster(game_ref)
        r.relative_position = relative_position
        r.direction = direction
        r.power = power
        return r

class Spaceship(Game_Object):
    def __init__(self,game_ref = None, silent=False):
        super().__init__(game_ref,silent=silent)
        self.name = "spaceship1"
        self.hull = 100
        self.shield = 100
        self.operating_system = docker_manager.get_os_name("test")
        self.started = False
        self.location = np.array([0,0,0])
        self.rotation = np.array([0,0,0])
        self.thrusters = []
        #self.test_thrusters()

    def test_thrusters(self):
        self.thrusters.append(Thruster.new(self.game_ref, np.array([-1,0,0]), np.array([0,0,0]), 10))
        self.thrusters.append(Thruster.new(self.game_ref, np.array([0,1,0]), np.array([0,0,0]), 1))
        self.thrusters.append(Thruster.new(self.game_ref, np.array([0,-1,0]), np.array([0,0,0]), 1))

    def start(self):
        if self.started:
            return
        self.started = True
        os = self.operating_system
        containers[self.id] = os.run()

    def is_running(self):
        if not self.started:
            return False
        if not containers[self.id]:
            print("Container not found")
            return False
        return docker_manager.is_container_running(containers[self.id])

    def attach_console(self):
        if not self.started:
            return
        container = containers[self.id]
        if not container:
            print("Container not found")
            return
        docker_manager.attach_console(container)

    def update(self, delta: float):
        if not self.started:
            return
        container = containers[self.id]
        assert container, "Container not found"
        sensor = {
            "update_time": self.game_ref.time,
        }

        plain_control = docker_manager.read_from_container(container, dir="/ship/", filename="control")
        docker_manager.write_to_container(container=container,content=json.dumps(sensor),  dir="/ship/", filename="sensor")
        if plain_control.strip() == "no data":
            return
        control = toml.loads(plain_control)
        print(control)

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

class Game:
    def __init__(self):
        self.initiated = False
        self.time = 0
        self.lock = threading.Lock()
        self.objectcount = 0
        self.objects = {}
        self.stopped = True
        self.start()

    def new_game():
        ret = Game()
        ret.player = Player(game_ref=ret)
        ret.initiated = True
        return ret

    def load_game(savegame_name):
        with open("resources/savegames/"+savegame_name, "r") as savegame:
            d = json.loads(savegame.read())
            return from_dict(d, None)

    def save_game(self,savegame_name):
        with open("resources/savegames/"+savegame_name, "w") as savegame:
            d = to_dict(self, forced=True)
            savegame.write(json.dumps(d))

    def update(self, delta: float):
        self.time += delta
        self.player.update(delta)

    def loop(self):
        running_time = -1
        while True:
            with self.lock:
                if self.initiated:
                    if self.stopped:
                        break
                    if running_time == -1:
                        running_time = time.time()
                    else:
                        time_ = time.time()
                        diff = time_ - running_time
                        running_time = time_
                        self.update(diff)

            time.sleep(1)

    def start(self):
        threading.Thread(target=self.loop).start()

def to_dict(obj, forced = False):
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
                    d[key] = [to_dict(obj, forced=True) for obj in obj.__dict__[key].values()]
                    continue
                d[key] = to_dict(obj.__dict__[key])
            return d
        else:
            d = {}
            d["type"] = "game_ref"
            return d

    if isinstance(obj, Game_Object):    
        if forced:
            d = {}
            d["type"] = "Game_Object"
            d["class"] = obj.__class__.__name__
            d["value"] = {key: to_dict(obj.__dict__[key]) for key in obj.__dict__}
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
    
    print("unknown type:",type(obj), obj)
    assert False, "something went wrong"

def from_dict(d, game_ref, no_ref = False, only_ref = False):
    assert type(d) == dict, "d is not a dict"
    assert "type" in d, "no type in dict"
    if d["type"] == "Game":
        r = Game()
        for obj in d["objects"]:
            r.objects[obj["value"]["id"]["value"]] = from_dict(obj,r, no_ref=True)
        for obj in d["objects"]:
            r.objects[obj["value"]["id"]["value"]] = from_dict(obj,r, only_ref=True)

        for key in d:
            if key == "type":
                continue
            if key == "objects":
                continue
            r.__dict__[key] = from_dict(d[key],r)
        return r
    if d["type"] == "game_ref":
        return game_ref
    if d["type"] == "Game_Object":
        if only_ref:
            r = game_ref.objects[d["value"]["id"]["value"]]
        else:
            cls = d["class"]
            r = globals()[cls](game_ref)
        for key in d["value"]:
            r.__dict__[key] = from_dict(d["value"][key], game_ref, no_ref=no_ref, only_ref=only_ref) 
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
    print(d["type"])

    assert False, "something went wrong"


#{key: id, v: docker_container}
containers = {}

### main 
if __name__ == "__main__":
    game = Game.new_game()
    game.player.spaceships.append(Spaceship())
    d = to_dict(game)
    game.running = False
    game.stopped = True
    print(len(game.objects))
    #print(d)
    
    #print("###########")
    game = from_dict(d, None)
    print(len(game.objects))



