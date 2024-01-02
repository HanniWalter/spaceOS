

from flask import Flask, redirect, url_for, render_template, request
import game_classes
from game_classes import Game, getSavegames, Spaceship, Player, game, docker_manager
app = Flask(__name__)


### Flask routes api ###
@app.route("/savegames", methods=["GET"])
def savegames():
    return {"savegames": getSavegames()}


@app.route("/game", methods=["GET"])
def game_data():
    return game.to_dict()


@app.route("/newgame", methods=["POST"])
def newgame():
    game.new_game()
    # return success
    return {"success": True}, 201


@app.route("/loadgame", methods=["POST"])
def loadgame():
    game = Game.load_game("savegame")
    # return success
    return {"success": True}, 201


@app.route("/savegame", methods=["POST"])
def savegame():
    savegame_name = "savegame"
    game.save_game(savegame_name)
    # return success
    return {"success": True}, 201


@app.route("/spaceship", methods=["PUT", "GET", "DELETE"])
def spaceship():
    global game
    id = request.json["id"]
    if request.method == "PUT":
        for spaceship in game.player.spaceships:
            if int(spaceship.id) == int(id):
                # update spaceship
                return {"success": True}, 201
        # create spaceship
        game.player.spaceships.append(Spaceship.from_dict(request.json))
        return {"success": True}, 201
    elif request.method == "GET":
        for spaceship in game.player.spaceships:
            if spaceship.id == id:
                # get spaceship
                return spaceship.to_dict()
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
    spaceship = game.player.get_spaceship(spaceship_id)
    if spaceship:
        spaceship.start()
        return {"success": True}, 201
    return {"success": False}, 404


@app.route("/attach_console/<int:spaceship_id>", methods=["POST"])
def attach_console(spaceship_id):
    global game
    spaceship = game.player.get_spaceship(spaceship_id)
    if spaceship:
        spaceship.attach_console()
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
    return render_template("main.html", game=game)


@app.route("/spaceship_creator")
def spaceship_creator():
    return "<p>Spaceship Creator</p>"


@app.route("/spaceships/<int:spaceship_id>")
def spaceships(spaceship_id):
    return "<p>Spaceship %d</p>" % spaceship_id


@app.route("/ShipDesigner/<int:spaceship_id>")
def ship_designer(spaceship_id):
    global game
    spaceship = game.player.get_spaceship(spaceship_id)
    if spaceship:
        return ship_designer_template(spaceship, new_ship=False)
    return "Spaceship not found", 404


@app.route("/ShipDesigner/new")
def ship_designer_new():
    return ship_designer_template(Spaceship(), new_ship=True)


def ship_designer_template(spaceship, new_ship):
    global game
    return render_template("ship_designer.html",
                           spaceship=spaceship, game=game, new_ship=new_ship, oss=docker_manager.oss)
