import numpy as np

from src.util import docker_manager
import src.gameobjects.Game_Object as Game_Object
import src.gameobjects.Thruster as Thruster
import toml

containers = {}


class Spaceship(Game_Object.Game_Object):
    def __init__(self, game_ref=None, silent=False):
        super().__init__(game_ref, silent=silent)
        self.name = "spaceship1"
        self.operating_system = docker_manager.get_os_name("test")
        self.started = False

        # self.test_thrusters()

    def new(game_ref,name, operating_system):
        r = Spaceship(game_ref, silent=False)
        r.name = name
        r.operating_system = docker_manager.get_os_name(operating_system)
        r.components = []
        r.location = np.array([0, 0, 0])
        r.rotation = np.array([0, 0, 0])

        return r

    def modify(self, modification_config):
        self.name = modification_config["name"]
        self.operating_system = docker_manager.get_os_name(modification_config["os"])

    def clone(self):
        r = Spaceship.new(self.game_ref, self.name, self.operating_system.name)

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

        for component in self.components:
            component.update2(delta)
            component.update(delta)
