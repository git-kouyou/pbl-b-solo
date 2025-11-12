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
import math
from collections import deque
from reachable import Reachable
from gamedata import Status, GameData
from simulation import Simulation

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data

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
def move_internal(data: GameData) -> typing.Dict:
    next_move = "None"

    #体が極小の時: 優先度1
    if data.length() <= 2:
        return {"move": random.choice(data.no_foods())}

    # 指定ルートがある場合(エサを探すとき): 優先度2
    if GameData.isDisignated:
        if GameData.disignated_route == 0:
            next_move = GameData.disignated_route.popleft()
            if DEBUG:
                print(f"Disignated Move: {next_move}")
            return {"move": next_move}
        else:
            GameData.isDisignated = False
            GameData.status = Status.loop

    starting_length = 0
    if 3 <= data.length() <= 4:
        starting_length = 12
    elif data.length() <= 9:
        starting_length = 9
    elif data.length() <= 17:
        starting_length = 12
    else:
        starting_length = 20

    # 体力が少ないときのエサ探索: 優先度3
    if data.health <= starting_length:
        simulator = Simulation(game_data = data, max_depth = data.health)
        simulator.route_search_new(data = data)
        if simulator.result_tire1:
            GameData.disignated_route = max(simulator.result_tire1, key = len)
            print(f"Tire 1 route: {GameData.disignated_route}")
        elif simulator.result_tire2:
            GameData.disignated_route = max(simulator.result_tire2, key = len)
            print(f"Tire 2 route: {GameData.disignated_route}")
        elif simulator.result_tire3:
            GameData.disignated_route = min(simulator.result_tire3, key = len)
            print(f"Tire 3 route: {GameData.disignated_route}")

        if GameData.isDisignated == False and GameData.disignated_route:
            GameData.isDisignated = True
            GameData.status = Status.eat_food
            next_move = GameData.disignated_route.popleft()
            if DEBUG:
                print(f"Disignated Move: {next_move}")
            return {"move": next_move}
        
    # 進行可能方向がないor一つしかない場合の処理: 優先度4
    if len(data.safes_around()) == 0:
        if len(data.empty_around()) > 0:
            next_move = random.choice(data.empty_around())
        else:
            if DEBUG:
                print("No safe move detected! move down!")
            next_move = "down"
        return {"move": next_move}
    elif len(data.safes_around()) == 1:
        if DEBUG:
            print("Only one safe move detected!")
        next_move = data.safes_around()[0]
        return {"move": next_move}

    # ループを探す動作: 優先度5
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
            next_move = max(next, key = lambda x: distance[x])
        elif len(next) == 1:
            next_move = next[0]
        else:
            #TODO: 尻尾に到達可能な方向を探す
            for move in data.no_foods():
                next_head = data.next_head_position(data.head(), move)
                new_body = data.bodies.copy()
                new_body.popleft()
                new_body.appendleft(next_head)
                if Reachable(bodies = new_body, foods = data.foods, width = GameData.board_width, height = GameData.board_height).is_reachable_tail_food_avoidance(next_head):
                    next_move = move
                    return {"move": next_move}
                elif Reachable(bodies = new_body, foods = data.foods, width = GameData.board_width, height = GameData.board_height).is_reachable_tail(next_head):
                    next_move = move
                    return {"move": next_move}
                elif data.no_foods():
                    next_move = random.choice(data.no_foods())
                    return {"move": next_move}
                elif data.safes_around():
                    next_move = random.choice(data.safes_around())
                    return {"move": next_move}
    
    if next_move == "None" and data.safes_around():
        next_move = random.choice(data.safes_around())
    return {"move": next_move}

# 初期化やデバッグ表示など
def move(game_state: typing.Dict) -> typing.Dict:
    data = GameData(game_state)
    #data.print_board()
    next_move =  move_internal(data)
    GameData.previous_foods = data.foods
    
    reachable_food_avoidance = []
    reachable = []
    if data.length() >= 3:
        for move in data.safes_around():
            next_head = data.next_head_position(data.head(), move)
            new_body = data.bodies.copy()
            new_body.pop()
            new_body.appendleft(next_head)
            if Reachable(bodies = new_body, foods = data.foods, width = GameData.board_width, height = GameData.board_height).is_reachable_tail_food_avoidance(next_head):
                reachable_food_avoidance.append(move)
    if data.length() >= 3:
        for move in data.safes_around():
            next_head = data.next_head_position(data.head(), move)
            new_body = data.bodies.copy()
            new_body.pop()
            new_body.appendleft(next_head)
            if Reachable(bodies = new_body, foods = data.foods, width = GameData.board_width, height = GameData.board_height).is_reachable_tail(next_head):
                reachable.append(move)
    if DEBUG:
        print(f"reachable: {reachable} reachable_food_avoidance: {reachable_food_avoidance}")
        print(f"no foods: {data.no_foods()}")
        print(f"safes around: {data.safes_around()}")
        print(f"MOVE {game_state['turn']}: {next_move}")
        print(f"頭: {data.head()} 現在のステータス: {GameData.status}")
    return next_move  

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
