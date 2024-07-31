import app
from src.gameobjects.Game import Game


@app.app.route("/newgame", methods=["POST"])
def newgame():

    app.game = Game.new_game()
    # create random admin passwort
    admin_password = app.session_manager.admin_password
    # return success
    return {"success": True, "admin_passwort": admin_password}, 201


@app.app.route("/deleteGame", methods=["POST"])
def deleteGame():

    app.game = None
    return {"success": True}, 201
