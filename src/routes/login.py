from app import app, session_manager, game
from flask import request
from src.gameobjects.Player import Player


@app.route("/register", methods=["POST"])
def registerPlayer():
    global game
    with game.lock:
        name = request.json["name"]
        password = request.json["password"]
        player = Player.Player.new(game_ref=game, name=name, password=password)
        if player:
            session_id = session_manager.new_session(player)
            return {"success": True, "player_id": player.id, "session_id": session_id}, 201
        else:
            return {"success": False, "error": "player already exists"}, 409


@app.route("/login", methods=["POST"])
def login():
    global game
    with game.lock:
        name = request.json["name"]
        password = request.json["password"]
        for player in game.players:
            if player.name == name:
                if player.login(password):
                    session_id = session_manager.new_session(player)
                    return {"success": True, "playerId": player.id, "session_id": session_id}, 200
                else:
                    return {"success": False}, 401
        return {"success": False}, 404
