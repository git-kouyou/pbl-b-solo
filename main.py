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
import predicates
import direction
from gamedata import Status, GameData
import gamedata

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
    neck_direction = None

    #体が極小の時
    if data.length() <= 2:
        data.set_target_food_random()
        return {"move": random.choice(data.safes_around())}

    # 進行可能方向がないor一つしかない場合の処理
    if data.length() <= 2:
        return {"move": random.choice(data.safes_around())}
    elif data.length() == 0:
        print("No safe move detected! move down!")
        next_move = "down"
        return {"move": next_move}
    elif data.length() == 1:
        next_move = data.safes_around()[0]
        return {"force move": next_move}

    if not(set(data.foods) == set(GameData.previous_foods)):
        GameData.status = Status.loop
        data.set_target_food_random()

    if GameData.status == Status.find_food:
        if abs(data.target_food[0] - data.head()[0]) <= 1 and abs(data.target_food[1] - data.head()[1]) <= 1:
            GameData.status = Status.loop
        elif(len(data.no_foods()) == 1):
            next_move = data.no_foods()[0]
        elif len(data.foods_and_unsafes()) == 4:
            pass
        elif data.target_food[0] < data.head()[0]:
            if "left" in data.foods_and_unsafes():
                if "up" in data.safes_around():
                    next_move = "up"
                elif "down" in data.safes_around():
                    next_move = "down"
            elif "left" in data.no_foods():
                next_move = "left"
        elif data.target_food[0] > data.head()[0]:
            if "right" in data.foods_and_unsafes():
                if "up" in data.safes_around():
                    next_move = "up"
                elif "down" in data.safes_around():
                    next_move = "down"
            elif "right" in data.no_foods():
                next_move = "right"
        elif data.target_food[1] < data.head()[1]:
            if "down" in data.foods_and_unsafes():
                if "left" in data.safes_around():
                    next_move = "left"
                elif "right" in data.safes_around():
                    next_move = "right"
            elif "down" in data.no_foods():
                next_move = "down"
        elif GameData.target_food[1] > data.head()[1]:
            if "up" in data.foods_and_unsafes():
                if "left" in data.safes_around():
                    next_move = "left"
                elif "right" in data.safes_around():
                    next_move = "right"
            elif "up" in data.no_foods():
                next_move = "up"
    
    if GameData.status == Status.loop:
        if game_state["you"]["health"] <= 2:
            GameData.status = Status.eat_food
        if data.tail()[0] < data.head()[0] and "left" in data.no_foods():
            next_move = "left"
        elif data.tail()[0] > data.head()[0] and "right" in data.no_foods():
            next_move = "right"
        elif data.tail()[1] < data.head()[1] and "down" in data.no_foods():
            next_move = "down"
        elif data.tail()[1] > data.head()[1] and "up" in data.no_foods():
            next_move = "up"
        elif data.heading() in data.no_foods():
            next_move = data.heading()
        else:
            if len(data.safes_around()) > 0:
                next_move = random.choice(data.safes_around())

    if GameData.status == Status.eat_food:
        result = []
        gamedata.route_search_rec(max_depth=data.length(), data = data, result = result)
        print(result)

    if next_move == "None":
        print("random move")
        next_move = random.choice(data.safes_around())

    print(f"MOVE {game_state['turn']}: {next_move}")
    print(f"頭: {data.head()} ターゲットの食べ物: {GameData.target_food} 現在のステータス: {GameData.status}")
    GameData.previous_foods = data.foods
    return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
