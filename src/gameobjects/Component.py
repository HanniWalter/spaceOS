from src.gameobjects.Game_Object import Game_Object 
from src.util import docker_manager
import toml

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
        if self.creates_logs:   
            self.write_log()
        if self.reads_config:
            self.config = self.read_config()
        print("test update")

    def read_config(self):
        container = self.parent.get_container()
        return docker_manager.read_from_container(container, dir=f"/ship/{self.id}/", filename="config")

    def write_log(self):
        sensor = self.log_data()
        content_toml = toml.dumps(sensor)
        container = self.parent.get_container()
        docker_manager.write_to_container(container, dir=f"/ship/{self.id}/", filename="log", content=content_toml)



    def on_start(self):
        pass        

#gets the current time
#not configurable    
class Clock(Component):
    def __init__(self, parent: Game_Object, game_ref = None, silent = False):
        reads_config = False
        creates_logs = True
        super().__init__(parent, game_ref, silent, creates_logs, reads_config)


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

#gets the current location
#not configurable maybe later
class Logbook(Component):
    pass