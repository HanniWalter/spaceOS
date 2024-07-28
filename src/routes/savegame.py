from app import app, game
from flask import request
from src.gameobjects.Game import Game


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
