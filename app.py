

from flask import Flask, redirect, url_for, render_template, request
import glob

from src.gameobjects.Game import Game
from src.gameobjects.Spaceship import Spaceship
from src.util import docker_manager

#import game_classes
#from game_classes import getSavegames, docker_manager

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


#@app.route("/game", methods=["GET"])
#def game_data():
#    with game.lock: 
#        return game.to_dict()


@app.route("/newgame", methods=["POST"])
def newgame():
    global game
    game = Game.new_game()
    # return success
    return {"success": True}, 201


@app.route("/loadgame", methods=["POST"])
def loadgame():
    global game
    game = Game.load_game("savegame")
    # return success
    return {"success": True}, 201


@app.route("/savegame", methods=["POST"])
def savegame():
    with game.lock:
        savegame_name = "savegame"
        game.save_game(savegame_name)
        # return success
        return {"success": True}, 201


@app.route("/spaceship", methods=["PUT", "DELETE"])
def spaceship():
    global game
    with game.lock:
        id = request.json["id"]
        if request.method == "PUT":
            # create spaceship
            if request.json["id"] == "":
                print("new spaceship")
                ship = Spaceship(game_ref=game)
                ship.apply_template(request.json)
                game.player.spaceships.append(ship)
            else:
                print("update spaceship")
                ship = game.objects[int(request.json["id"])]
                ship.apply_template(request.json)
            
            return {"success": True}, 201
        #elif request.method == "GET":
        #    for spaceship in game.player.spaceships:
        #        if spaceship.id == id:
        #            # get spaceship
        #            return spaceship.to_dict()
            # return error
            return {"success": False}, 404
        elif request.method == "DELETE":
            for spaceship in game.player.spaceships:
                if spaceship.id == id:
                    # delete spaceship
                    game.player.spaceships.remove(spaceship)
                    return {"success": True}, 201
            # return error
            return {"success": False}, 404


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
        return render_template("main.html",oss = docker_manager.oss, game=game)


@app.route("/spaceships/<int:spaceship_id>")
def spaceships(spaceship_id):
    with game.lock:
        return "<p>Spaceship %d</p>" % spaceship_id



@app.route("/ShipDesigner/<int:spaceship_id>")
def ship_designer(spaceship_id):
    with game.lock:
        spaceship = game.player.get_spaceship(spaceship_id)
        if spaceship:
            return ship_designer_template(spaceship, new_ship=False)
        return "Spaceship not found", 404


@app.route("/ShipDesigner/new")
def ship_designer_new():
    with game.lock:
        return ship_designer_template(Spaceship(silent=True), new_ship=True)


def ship_designer_template(spaceship, new_ship):
        return render_template("ship_designer.html",
                           spaceship=spaceship, game=game, new_ship=new_ship, oss=docker_manager.oss)
