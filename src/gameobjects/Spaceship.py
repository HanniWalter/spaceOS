import numpy as np

from src.util import docker_manager
from src.gameobjects.Game_Object import Game_Object
from src.gameobjects.Thruster import Thruster
import toml  

containers = {}

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

        self.components = []
        #self.test_thrusters()

    def start(self):
        if self.started:
            return
        self.started = True
        os = self.operating_system
        containers[self.id] = os.run()

        for component in self.components:
            component.create_files()
            component.on_start()

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

    def get_container(self):
        return containers[self.id]

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

