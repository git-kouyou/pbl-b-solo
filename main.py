# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
from gamedata import Status, GameData
from simulation import Simulation

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data

board_width = 0
board_height = 0
wall = []
body_length = 0
target_food = ()
previous_foods = []
status = Status.loop
DEBUG = True

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "6",  # TODO: Your Battlesnake Username
        "color": "#FFC0CB",  # TODO: Choose color pink
        "head": "pig",  # TODO: Choose head
        "tail": "football",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    GameData(game_state)
    print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    data: GameData = GameData(game_state)
    next_move = "None"

    #体が極小の時
    if data.length() <= 2:
        return {"move": random.choice(data.no_foods())}
    
    if len(GameData.disignated_route) == 0 and GameData.isDisignated:
        GameData.isDisignated = False
        GameData.status = Status.loop

    if GameData.isDisignated:
        next_move = GameData.disignated_route.pop(0)
        if DEBUG:
            print(f"Disignated Move: {next_move}")
        return {"move": next_move}

    if game_state["you"]["health"] <= 10:
        simulator = Simulation(game_data = data, max_depth = game_state["you"]["health"])
        simulator.route_search_12(data = data)
        if(len(simulator.result) > 0):
            GameData.disignated_route = max(simulator.result, key = len)
            GameData.isDisignated = True
            GameData.status = Status.eat_food
            next_move = GameData.disignated_route.pop(0)
            if DEBUG:
                print(f"Disignated Move: {next_move}")
            return {"move": next_move}
        
    # 進行可能方向がないor一つしかない場合の処理
    if len(data.safes_around()) == 0:
        if DEBUG:
            print("No safe move detected! move down!")
        next_move = "down"
        return {"move": next_move}
    elif len(data.safes_around()) == 1:
        if DEBUG:
            print("Only one safe move detected!")
        next_move = data.safes_around()[0]
        return {"move": next_move}

    if GameData.status == Status.loop:
        next = []
        distance = {"up": data.tail()[1] - data.head()[1],
                    "down": data.head()[1] - data.tail()[1],
                    "right": data.tail()[0] - data.head()[0],
                    "left": data.head()[0] - data.tail()[0]}
        
        for move in data.no_foods():
            if distance[move] > 0:
                next.append(move)
        if len(next) == 2:
            next = [max(next, key = lambda x: distance[x])]
        elif len(next) == 0:
            next = data.no_foods()
        if len(next) > 0:
            next_move = random.choice(next)
        else:
            next_move = random.choice(data.safes_around())

    if next_move == "None":
        print("random move")
        next_move = random.choice(data.safes_around())
    if DEBUG:
        print(f"no foods: {data.unsafes_around()}")
        print(f"MOVE {game_state['turn']}: {next_move}")
        print(f"頭: {data.head()} 現在のステータス: {GameData.status}")
    GameData.previous_foods = data.foods
    return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
