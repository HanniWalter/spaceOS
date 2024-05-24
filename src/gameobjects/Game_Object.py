
class Game_Object:
    # you may ask what is silent for?
    # it is for the loading of the game from a file without creating the infinite loops of objects
    # it is a bit hacky but it works
    def __init__(self, game_ref=None, silent=False):
        if silent:
            return
        assert game_ref, "game_ref is needed in nonsilent mode"
        self.id = game_ref.objectcount
        game_ref.objectcount += 1
        game_ref.objects[self.id] = self

        self.game_ref = game_ref
        self.components = []

    # todo:
    # add here a lot of work for example it is not possible to change the os
    def apply_template(self, template):
        for key in template:
            if key in self.__dict__:
                if type(self.__dict__[key]) != type(template[key]):
                    return
            self.__dict__[key] = template[key]
