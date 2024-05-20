import glob
import json
import random
import src.docker_manager as docker_manager
import threading
import time
import numpy as np
import toml
from gameobjects.Game_Object import Game_Object as Game_Object 
### Game logic ###


def getSavegames():
    savegames = []
    for savegame in glob.glob("resources/savegames/*"):
        savegames.append(savegame)
    return savegames


    


#{key: id, v: docker_container}
containers = {}

### main 




