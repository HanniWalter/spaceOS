import app
from flask import request
from src.gameobjects.Game import Game
import json


@app.app.route("/loadgame", methods=["POST"])
def loadgame():
    app.game = Game.Game.load_game("savegame")
    # return success
    return {"success": True}, 201


@app.app.route("/getSavegame", methods=["POST"])
def getSavegame():
    with app.game.lock:
        savegame_name = request.json["savegame_name"]
        data = app.game.saveGameData(savegame_name)
        # return success
        return {"success": True, "savegame": json.dumps(data)}, 201


@app.app.route("/saveSavegame", methods=["POST"])
def saveSavegame():
    save = request.json["savegame"]
    name = json.loads(save)["savegame_name"]

    # creating new or overwriting savegame
    with open("resources/savegames/"+name, "w") as savegame:
        savegame.write(save)

    return {"success": True}, 201
