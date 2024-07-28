from app import app, session_manager, game
from flask import render_template, redirect, url_for


@app.route("/")
def index():
    # redirect to main menu
    return redirect(url_for('mainMenu'))


@app.route("/mainMenu")
def mainMenu():
    game_exists = game is not None
    return render_template("menu/mainMenu.html", game_exists=game_exists)


@app.route("/joinGame/<string:local_ip>/<int:local_port>")
def joinGame(local_ip, local_port):
    global game
    players = game.players
    return render_template("menu/joinGame.html", players=players, local_ip=local_ip, local_port=local_port, admin=False)


@app.route("/joinGameAdmin/<string:local_ip>/<int:local_port>/<string:admin_password>")
def joinGameAdmin(local_ip, local_port, admin_password):
    if str(admin_password) == str(session_manager.admin_password):
        return render_template("menu/joinGame.html", local_ip=local_ip, local_port=local_port, admin=True, admin_password=admin_password)
    else:
        return "Unauthorized", 401


@app.route("/joinMultiplayer")
def joinMultiplayer():
    return render_template("menu/joinMultiplayer.html")
