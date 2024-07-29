import app
from flask import request
from src.gameobjects.Game import Game
import json

import glob
import json
import time
from flask_cors import cross_origin


def getSavegames():
    savegames = []
    for savegame in glob.glob("resources/savegames/*"):
        # read name and date from savegame json
        data = json.load(open(savegame))
        name = data["savegame_name"]
        # convert timestamp to human readable date
        time_ = time.strftime("%d.%m.%Y %H:%M:%S",
                              time.localtime(data["time"]))
        savegame = {"name": data["savegame_name"], "time": time_}
        savegames.append(savegame)
    return savegames


@app.app.route("/loadGame", methods=["POST"])
def loadgame():
    name = request.json["savegame_name"]
    savegame = json.load(open("resources/savegames/"+name))
    app.game = Game.load_game(savegame)
    # return success
    return {"success": True}, 201


@app.app.route("/getSavegameData", methods=["GET"])
@cross_origin()
def getSavegameData():
    # allow cross origin requests
    savegameData = getSavegames()
    return {"success": True, "savegame_data": savegameData}, 201


@app.app.route("/getSavegame", methods=["POST"])
def getSavegame():
    with app.game.lock:
        savegame_name = request.json["savegame_name"]
        data = app.game.saveGameData(savegame_name)
        # return success
        return {"success": True, "savegame": json.dumps(data)}, 201


@app.app.route("/saveSavegame", methods=["POST"])
@cross_origin()
def saveSavegame():
    save = request.json["savegame"]
    name = json.loads(save)["savegame_name"]

    # creating new or overwriting savegame
    with open("resources/savegames/"+name, "w") as savegame:
        savegame.write(save)

    return {"success": True}, 201
