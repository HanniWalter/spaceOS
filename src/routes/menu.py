import app
from flask import render_template, redirect, url_for


@app.app.route("/")
def index():
    # redirect to main menu
    return redirect(url_for('mainMenu'))


@app.app.route("/mainMenu")
def mainMenu():
    game_exists = app.game is not None
    return render_template("menu/mainMenu.html", game_exists=game_exists)


@app.app.route("/saveGameMenu")
def saveGameMenu():
    return render_template("menu/saveGameMenu.html")


@app.app.route("/loadGameMenu")
def loadGameMenu():
    return render_template("menu/loadGameMenu.html")


@app.app.route("/joinGame/<string:local_ip>/<int:local_port>")
def joinGame(local_ip, local_port):
    players = app.game.players
    return render_template("menu/joinGame.html", players=players, local_ip=local_ip, local_port=local_port, admin=False)


@app.app.route("/joinGameAdmin/<string:local_ip>/<int:local_port>/<string:admin_password>")
def joinGameAdmin(local_ip, local_port, admin_password):
    if str(admin_password) == str(app.session_manager.admin_password):
        return render_template("menu/joinGame.html", local_ip=local_ip, local_port=local_port, admin=True, admin_password=admin_password)
    else:
        return "Unauthorized", 401


@app.app.route("/joinMultiplayer")
def joinMultiplayer():
    return render_template("menu/joinMultiplayer.html")


@app.app.route("/deleteGameConfirmation")
def deleteGameConfirmation():
    return render_template("menu/deleteConfirmation.html")
