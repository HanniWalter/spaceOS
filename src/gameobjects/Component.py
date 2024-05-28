import src.gameobjects as gameobjects
#from src.gameobjects.Game_Object import Game_Object
from src.util import docker_manager
#from src.gameobjects.Spaceship import Spaceship
import toml
import numpy as np
import src.gameobjects.Game_Object as Game_Object

class Component(Game_Object.Game_Object):
    def __init__(self, game_ref=None, silent=False):
        super().__init__(game_ref, silent)

    def initialise(self, parent: gameobjects.Spaceship, creates_logs=False, reads_config=False):
        r = self

        r.reads_config = reads_config
        r.creates_logs = creates_logs
        r.parent = parent
        r.parent.components.append(r)

    def create_files(self):
        container = self.parent.get_container()
        if self.creates_logs:
            # create log file
            docker_manager.create_file_in_container(
                container, dir=f"/ship/{self.id}/", filename="log")
            docker_manager.write_to_container(
                container, dir=f"/ship/{self.id}/", filename="log", content="no data")
        if self.reads_config:
            # create config file
            docker_manager.create_file_in_container(
                container, dir=f"/ship/{self.id}/", filename="config")
            docker_manager.write_to_container(
                container, dir=f"/ship/{self.id}/", filename="config", content="no data")

    def update2(self, delta: float):
        if self.creates_logs:
            self.write_log()
        if self.reads_config:
            self.config = self.read_config()

    def read_config(self):
        container = self.parent.get_container()
        config = docker_manager.read_from_container(
            container, dir=f"/ship/{self.id}/", filename="config")
        if config == "no data":
            return {"error": "no data"}

        config = toml.loads(config)

        return config

    def write_log(self):
        sensor = self.log_data()
        content_toml = toml.dumps(sensor)
        container = self.parent.get_container()
        docker_manager.write_to_container(
            container, dir=f"/ship/{self.id}/", filename="log", content=content_toml)

    def on_start(self):
        pass

    def update(self, delta: float):
        pass

    def log_data(self):
        return {}

# gets the current time
# not configurable


class Teleporter(Component):
    def __init__(self, game_ref=None, silent=False):
        super().__init__(game_ref, silent)
        self.next_job_id = 0

    def new(parent: gameobjects.Spaceship, game_ref):
        r = Teleporter(game_ref=game_ref)
        r.initialise(parent, creates_logs=True, reads_config=True)
        return r

    def update(self, delta: float):
        if "error" in self.config:
            return
        if self.config["next_job_id"] == self.next_job_id:
            self.next_job_id = self.config["next_job_id"] + 1
            locationx = self.config["location"][0]
            locationy = self.config["location"][1]
            locationz = self.config["location"][2]
            self.parent.location = np.array([locationx, locationy, locationz])

    def log_data(self):
        sensor = {
            "type": "teleporter",
            "next_job_id": self.next_job_id,
            "location": self.parent.location,
        }
        return sensor


class Clock(Component):
    def __init__(self, game_ref=None, silent=False):
        super().__init__(game_ref, silent)

    def new(parent: gameobjects.Spaceship, game_ref):
        r = Clock(game_ref=game_ref)
        r.initialise(parent, creates_logs=True, reads_config=False)
        return r

    def on_start(self):
        self.start_time = self.get_time()

    def get_time(self):
        return self.game_ref.time

    def log_data(self):
        sensor = {
            "type": "clock",
            "id": self.id,
            "global_time": self.get_time(),
            "start_time": self.start_time,
            "local_time": self.get_time() - self.start_time,
        }
        return sensor

# gets the current location
# not configurable maybe later


class Logbook(Component):
    pass
