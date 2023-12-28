import glob
import json
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

### Game logic ###
def getSavegames():
    savegames = []
    for savegame in glob.glob("resources/savegames/*"):
        savegames.append(savegame)
    return savegames

class Spaceship:
    def __init__(self):
        self.name = "spaceship1"
        self.hull = 100
        self.shield = 100
        self.weapons = []
        self.cargo = []

    def to_dict(self):
        return {
            "name": self.name,
            "hull": self.hull,
            "shield": self.shield,
            "weapons": self.weapons,
            "cargo": self.cargo
        }

    def from_dict(spaceship_dict):
        spaceship = Spaceship()
        spaceship.name = spaceship_dict["name"]
        spaceship.hull = spaceship_dict["hull"]
        spaceship.shield = spaceship_dict["shield"]
        spaceship.weapons = spaceship_dict["weapons"]
        spaceship.cargo = spaceship_dict["cargo"]
        return spaceship
    
class Player:
    def __init__(self):
        self.name = "player1"
        self.spaceships = []
        self.money = 1000
    
    def to_dict(self):
        return {
            "name": self.name,
            "spaceships": [spaceship.to_dict() for spaceship in self.spaceships],
            "money": self.money
        }
    
    def from_dict(player_dict):
        player = Player()
        player.name = player_dict["name"]
        player.spaceships = [Spaceship.from_dict(spaceship_dict) for spaceship_dict in player_dict["spaceships"]]
        player.money = player_dict["money"]
        return player

class Game:
    def __init__(self):
        self.initiated = False

    def new_game(self):
        self.initiated = True
        self.player = Player()


    def load_game(savegame_name):
        #load game from file
        with open("resources/savegames/"+savegame_name, "r") as savegame:
            game.from_dict(json.loads(savegame.read()))

    def save_game(self, savegame_name = "savegame"):
        #save game to file
        with open("resources/savegames/"+savegame_name, "w") as savegame:
            savegame.write(json.dumps(self.to_dict()))


    def to_dict(self):
        if self.initiated:
            return {
                "initiated": self.initiated,
                "player": self.player.to_dict()
            }
        else:
            return {
                "initiated": self.initiated
            }

    def from_dict(self,game_dict):
        self.initiated = game_dict["initiated"]
        self.player = Player.from_dict(game_dict["player"])

game = Game()

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
    #return success
    return {"success": True}, 201

@app.route("/loadgame", methods=["POST"])
def loadgame():
    game = Game.load_game("savegame")
    #return success
    return {"success": True}, 201

@app.route("/savegame", methods=["POST"])
def savegame():
    savegame_name = "savegame"
    game.save_game("savegame")
    #return success
    return {"success": True}, 201



### Flask routes web ###
@app.route("/")
def hello_world():
    #redirect to main menu
    return redirect(url_for('main_menu'))

@app.route("/main_menu")
def main_menu():
    return render_template("main_menu.html")

@app.route("/main")
def main():
    return render_template("main.html", game=game)

@app.route("/spaceship_creator")
def spaceship_creator():
    return "<p>Spaceship Creator</p>"

@app.route("/spaceships/")
def spaceships():
    return "<p>Spaceships</p>"

@app.route("/spaceships/<int:spaceship_id>")
def spaceship(spaceship_id):
    return "<p>Spaceship %d</p>" % spaceship_id
