from Game_Object import Game_Object as Game_Object

class Component(Game_Object):
    def __init__(self,parent: Game_Object, game_ref = None, silent = False):
        super().__init__(game_ref, silent)

        parent.components.append(self)

    def update(self, delta: float):
        self.write_log()

    def read_config(self):
        pass

    def write_log(self):
        pass

    
class Clock(Component):
    pass

class Logbook(Component):
    pass