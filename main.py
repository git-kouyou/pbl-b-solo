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
from enum import Enum

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
class Status(Enum):
    food = 0
    loop = 1

board_width = 0
board_height = 0
wall = []
body_length = 0
target_food = ()
status = Status.food 

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
    global board_height, board_width, wall, body_length
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    wall1 = [(x, -1) for x in range(-1, board_width + 1)]
    wall2 = [(x, board_height) for x in range(-1, board_width + 1)]
    wall3 = [(-1, y) for y in range(board_height)]
    wall4 = [(board_width, y) for y in range(board_height)]
    wall = wall1 + wall2 + wall3 + wall4

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    global board_width, board_height, wall, status, body_length, target_food
    next_move = None
    neck_direction = None

    bodies = [(body["x"], body["y"]) for body in game_state["you"]["body"]]
    foods = [(food["x"], food["y"]) for food in game_state["board"]["food"]]
    print(f"食べ物の位置: {foods}")
    unsafe_zones = bodies + wall

    my_head = (game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
    if len(game_state["you"]["body"]) > body_length:
        my_neck = (game_state["you"]["body"][1]["x"], game_state["you"]["body"][1]["y"])
        target_food = random.choice(foods)
        print(f"ターゲットの食べ物: {target_food}")
        neck_direction = predicates.neck_direction(my_head, my_neck)

    # 体と壁を避ける
    unsafes_around = predicates.unsafes_around({"x": my_head[0], "y": my_head[1]}, unsafe_zones)

    # 食べ物
    foods_around = predicates.foods_around({"x": my_head[0], "y": my_head[1]}, foods)

    # 食べ物と体と壁
    foods_and_unsafes = list(set(foods_around) | set(unsafes_around))

    # 安全地帯
    safes_around = list(set(["up", "down", "left", "right"]) - set(unsafes_around))

    # 食べ物なし
    no_foods = list(set(safes_around) - set(foods_around))

    #体が極小の時
    if len(game_state['you']['body']) <= 2:
        target_food = random.choice(foods)

    #体がでかくなった時
    if len(game_state['you']['body']) > body_length:
        body_length = len(game_state['you']['body'])
        target_food = random.choice(foods)
        status = Status.food

    # 進行可能方向がないor一つしかない場合の処理
    if len(game_state["you"]["body"]) <= 2:
        return {"move": random.choice(safes_around)}
    elif len(safes_around) == 0:
        print("No safe move detected! move down!")
        next_move = "down"
        return {"move": next_move}
    elif len(safes_around) == 1:
        next_move = safes_around[0]
        return {"move": next_move}

    if status == Status.food or status == Status.loop:
        if target_food not in foods:
            target_food = random.choice(foods)
            print(f"ターゲットの食べ物: {target_food}")

        if len(foods_and_unsafes) == 4:
            next_move = random.choice(safes_around)
        elif target_food[0] < my_head[0]:
            if "left" in foods_and_unsafes:
                if "up" in safes_around:
                    next_move = "up"
                elif "down" in safes_around:
                    next_move = "down"
            elif "left" in no_foods:
                next_move = "left"
        elif target_food[0] > my_head[0]:
            if "right" in foods_and_unsafes:
                if "up" in safes_around:
                    next_move = "up"
                elif "down" in safes_around:
                    next_move = "down"
            elif "right" in no_foods:
                next_move = "right"
        elif target_food[1] < my_head[1]:
            if "down" in foods_and_unsafes:
                if "left" in safes_around:
                    next_move = "left"
                elif "right" in safes_around:
                    next_move = "right"
            elif "down" in no_foods:
                next_move = "down"
        elif target_food[1] > my_head[1]:
            if "up" in foods_and_unsafes:
                if "left" in safes_around:
                    next_move = "left"
                elif "right" in safes_around:
                    next_move = "right"
            elif "up" in no_foods:
                next_move = "up"
        else:
            return {"move": random.choice(no_foods)}


    # if wall_count == 1:
    #     if neck == "left":
    #         next_move = "right"
    #     elif neck == "right":
    #         next_move = "left"
    #     elif neck == "up":
    #         next_move = "down"
    #     elif neck == "down":
    #         next_move = "up"
    # elif wall_count == 2:

    if(next_move is None):
        next_move = random.choice(safes_around)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
    

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
