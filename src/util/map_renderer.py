from PIL import Image
from PIL import ImageDraw



def render_map(game, config):
    map_renderer = Map_Renderer(game, config)
    map_renderer.render()
    return map_renderer.img

class Map_Renderer:
    def __init__(self, game, config):
        self.game = game
        self.config = config
        self.height = config["height"]
        self.width = config["width"]
        self.central_location = (config["central_location"]["x"], config["central_location"]["y"])
        self.scale = config["scale"]
        self.img = Image.new('RGB', (self.width, self.height), color = (0xea, 0xdd, 0xcd))
    
    def render(self):
        for ship in self.game.player.spaceships:
            self.render_ship(ship)

    def transform_location(self, location):
        x = (location[0] - self.central_location[0])/ self.scale + self.width / 2
        y = (location[1] - self.central_location[1])/ self.scale + self.height / 2 
        return (x, y)
    


    def render_ship(self,ship):
        #add a circle to the image
        location = self.transform_location((ship.location[0], ship.location[1]))
        radius = 10
        color = (0, 0, 255)

        draw = ImageDraw.Draw(self.img)
        draw.ellipse((location[0] - radius, location[1] - radius, location[0] + radius, location[1] + radius), fill=color)

def show_map(game):
    config = {
        "height": 600,
        "width": 600,
        "central_location": (0, 0),
        "scale": 4,
    }
    img = render_map(game, config)
    img.show()

