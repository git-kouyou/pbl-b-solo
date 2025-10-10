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

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
board_width = 0
board_height = 0
wall1 = []
wall2 = []
wall3 = []
wall4 = []

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")
    global board_height, board_width, wall1, wall2, wall3, wall4
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    wall1 = [(x, -1) for x in range(-1, board_width + 1)]
    wall2 = [(x, board_height) for x in range(-1, board_width + 1)]
    wall3 = [(-1, y) for y in range(board_height)]
    wall4 = [(board_width, y) for y in range(board_height)]


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    # We've included code to prevent your Battlesnake from moving backwards
    global board_width, board_height, wall1, wall2, wall3, wall4
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    checkmate = {"up": True, "down": True, "left": True, "right": True}
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    impossible = [(body["x"], body["y"]) for body in game_state["you"]["body"]]
    impossible += wall1 + wall2 + wall3 + wall4

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds

    # if my_head["x"] <= 0:
    #     is_move_safe["left"] = False

    # if my_head["x"] >= board_width - 1:
    #     is_move_safe["right"] = False

    # if my_head["y"] <= 0:
    #     is_move_safe["down"] = False

    # if my_head["y"] >= board_height - 1:
    #     is_move_safe["up"] = False

    #壁と自分の体にぶつからないようにする
    if (my_head["x"] - 1, my_head["y"]) in impossible:
        is_move_safe["left"] = False

    if (my_head["x"] + 1, my_head["y"]) in impossible:
        is_move_safe["right"] = False

    if (my_head["x"], my_head["y"] - 1) in impossible:
        is_move_safe["down"] = False

    if (my_head["x"], my_head["y"] + 1) in impossible:
        is_move_safe["up"] = False

    #詰みへ入らないようにする?
    if (my_head["x"] - 1, my_head["y"] + 1) in impossible and (my_head["x"] - 1, my_head["y"] - 1) in impossible:
        checkmate["left"] = False
        print("左無理")

    if (my_head["x"] + 1, my_head["y"] + 1) in impossible and (my_head["x"] + 1, my_head["y"] - 1) in impossible:
        checkmate["right"] = False
        print("右無理")

    if (my_head["x"] + 1, my_head["y"] + 1) in impossible and (my_head["x"] - 1, my_head["y"] + 1) in impossible:
        checkmate["up"] = False
        print("上無理")

    if (my_head["x"] + 1, my_head["y"] - 1) in impossible and (my_head["x"] - 1, my_head["y"] - 1) in impossible:
        checkmate["down"] = False
        print("下無理")

    # Are there any safe moves left?
    safe_moves = []
    if all(value == False for value in checkmate.values()):
        print("多分詰みやけど進むわ")
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)
    else:
        for move, isSafe in is_move_safe.items():
            if isSafe and checkmate[move]:
                safe_moves.append(move)

    # Choose a random move from the safe ones
    if len(safe_moves) == 0:
        print("No safe move detected! move down!")
        next_move = "down"
    else:
        next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    print(f"x:{my_head["x"]}, y:{my_head["y"]}")
    return {"move": next_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
