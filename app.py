

from flask import Flask, redirect, url_for, render_template, request
import glob
from base64 import b64encode
from io import BytesIO

import src.gameobjects as gameobjects
import src.gameobjects.Game as Game
import src.gameobjects.Spaceship as Spaceship
from src.util import docker_manager
from src.util import map_renderer
# import game_classes
# from game_classes import getSavegames, docker_manager

app = Flask(__name__)

game = None


def getSavegames():
    savegames = []
    for savegame in glob.glob("resources/savegames/*"):
        savegames.append(savegame)
    return savegames

### Flask routes api ###


@app.route("/savegames", methods=["GET"])
def savegames():
    return {"savegames": getSavegames()}


# @app.route("/game", methods=["GET"])
# def game_data():
#    with game.lock:
#        return game.to_dict()


@app.route("/newgame", methods=["POST"])
def newgame():
    global game
    game = Game.Game.new_game()
    # return success
    return {"success": True}, 201


@app.route("/loadgame", methods=["POST"])
def loadgame():
    global game
    game = Game.Game.load_game("savegame")
    # return success
    return {"success": True}, 201


@app.route("/savegame", methods=["POST"])
def savegame():
    with game.lock:
        savegame_name = "savegame"
        game.save_game(savegame_name)
        # return success
        return {"success": True}, 201


@app.route("/create_spaceship", methods=["POST"])
def create_spaceship():
    global game
    with game.lock:
        spaceship = game.player.spaceship_factory.build_spaceship()
        return {"id": spaceship.id}

@app.route("/clone_spaceship", methods=["POST"])
def clone_spaceship():
    global game
    with game.lock:
        spaceship = game.player.spaceship_factory.clone_spaceship()
        return {"id": spaceship.id}

@app.route("/modify_spaceship", methods=["POST"])
def modify_spaceship():
    global game
    with game.lock:
        spaceship = game.player.spaceship_factory.modify_spaceship()
        return {"id": spaceship.id}    

@app.route("/value_changed", methods=["POST"])
def value_changed():
    global game
    with game.lock:
        game.player.spaceship_factory.set_name(request.json["name"], request.json["new"])
        game.player.spaceship_factory.set_os(request.json["os"], request.json["new"])
        return {"success": True}, 201

@app.route("/start_spaceship/<int:spaceship_id>", methods=["POST"])
def start_spaceship(spaceship_id):
    global game
    with game.lock:
        spaceship = game.player.get_spaceship(spaceship_id)
        if spaceship:
            spaceship.start()
            return {"success": True}, 201
        return {"success": False}, 404


@app.route("/attach_console/<int:spaceship_id>", methods=["POST"])
def attach_console(spaceship_id):
    global game
    with game.lock:
        spaceship = game.player.get_spaceship(spaceship_id)
        if spaceship:
            spaceship.attach_console()
            return {"success": True}, 201


@app.route("/reload_oss", methods=["POST"])
def reload_oss():
    with game.lock:
        docker_manager.reload_oss()
        return {"success": True}, 201


@app.route("/build_os/<int:os_id>", methods=["POST"])
def build_os(os_id):
    with game.lock:
        os = docker_manager.get_os_id(int(os_id))
        if os:
            os.build_image(force=True)
            return {"success": True}, 201
        return {"success": False}, 404


@app.route("/map_image", methods=["POST"])
def get_map():
    render_config = request.json
    with game.lock:

        image = map_renderer.render_map(game, render_config)
        image_io = BytesIO()
        image.save(image_io, 'PNG')
        dataurl = 'data:image/png;base64,' + \
            b64encode(image_io.getvalue()).decode('ascii')
        return {"image": dataurl}


### Flask routes web ###
@app.route("/")
def index():
    # redirect to main menu
    return redirect(url_for('main_menu'))


@app.route("/main_menu")
def main_menu():
    return render_template("main_menu.html")


@app.route("/main")
def main():
    global game
    with game.lock:
        return render_template("main.html", oss=docker_manager.oss, game=game)


@app.route("/map")
def map():
    return render_template("map.html")


@app.route("/shipfactory/<int:spaceship_id>")
def ship_factory(spaceship_id):
    with game.lock:
        spaceship = game.player.get_spaceship(spaceship_id)
        if spaceship:
            game.player.spaceship_factory.prepare_modification_config(spaceship_id)
            return ship_factory_template(new_ship=False)
        return "Spaceship not found", 404


@app.route("/shipfactory/new")
def ship_factory_new():
    with game.lock:
        
        #spaceship_factory = game.player.get_spaceship_factory()
        return ship_factory_template(new_ship=True)


def ship_factory_template(new_ship):
    ship_factory_information = {}
    ship_factory_information["oss"] = game.player.spaceship_factory.get_oss()
    ship_factory_information["new_ship"] = new_ship
    #ship_factory_information["modules"] = []
    if new_ship:
        config = game.player.spaceship_factory.spaceship_config
    else:
        config = game.player.spaceship_factory.spaceship_modification_config
    return render_template("ship_factory.html", game=game, new_ship=new_ship, config = config, ship_factory_information=ship_factory_information)
