from src.gameobjects.Game_Object import Game_Object


class Thruster(Game_Object):
    def __init__(self, game_ref=None, silent=False):
        super().__init__(game_ref, silent)

    def new(game_ref, relative_position, direction, power):
        r = Thruster(game_ref)
        r.relative_position = relative_position
        r.direction = direction
        r.power = power
        return r
