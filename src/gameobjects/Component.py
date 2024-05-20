from src.gameobjects.Game_Object import Game_Object 
from src.util import docker_manager
class Component(Game_Object):
    def __init__(self,parent: Game_Object, game_ref = None, silent = False, creates_logs = False, reads_config = False):
        super().__init__(game_ref, silent)
        self.reads_config = reads_config
        self.creates_logs = creates_logs
        self.parent = parent
        parent.components.append(self)

    def create_files(self):
        container = self.parent.get_container()
        if self.creates_logs: 
            #create log file
            docker_manager.create_file_in_container(container, dir=f"/ship/{self.id}/", filename="log")
            docker_manager.write_to_container(container, dir=f"/ship/{self.id}/", filename="log", content="no data")
        if self.reads_config:
            #create config file
            docker_manager.create_file_in_container(container, dir=f"/ship/{self.id}/", filename="config")
            docker_manager.write_to_container(container, dir=f"/ship/{self.id}/", filename="config", content="no data")
    def update(self, delta: float):
        self.write_log()
        self.config = self.read_config()

    def read_config(self):
        pass

    def write_log(self):
        sensor = self.log_data()

    def on_start(self):
        pass        

#gets the current time
#not configurable    
class Clock(Component):
    def __init__(self, parent: Game_Object, game_ref = None, silent = False):
        reads_config = False
        creates_logs = True
        super().__init__(parent, game_ref, silent, creates_logs, reads_config)
        self.time = 0

    def log_data(self):
        sensor = {
            "time": self.time
        }
        return sensor

#gets the current location
#not configurable maybe later
class Logbook(Component):
    pass