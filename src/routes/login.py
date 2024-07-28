import app
from flask import request
from src.gameobjects.Player import Player


@app.app.route("/register", methods=["POST"])
def registerPlayer():
    with app.game.lock:
        name = request.json["name"]
        password = request.json["password"]
        player = Player.new(game_ref=app.game, name=name, password=password)
        if player:
            session_id = app.session_manager.new_session(player)
            return {"success": True, "player_id": player.id, "session_id": session_id}, 201
        else:
            return {"success": False, "error": "player already exists"}, 409


@app.app.route("/login", methods=["POST"])
def login():
    with app.game.lock:
        name = request.json["name"]
        password = request.json["password"]
        for player in app.game.players:
            if player.name == name:
                if player.login(password):
                    session_id = app.session_manager.new_session(player)
                    return {"success": True, "playerId": player.id, "session_id": session_id}, 200
                else:
                    return {"success": False}, 401
        return {"success": False}, 404
