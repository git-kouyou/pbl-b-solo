# 6班solo ソースコード
# python version: 3.13.3

import random
import typing
from reachable import Reachable
from gamedata import Status, GameData
from simulation import Simulation

X = 0
Y = 1

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
    GameData.initialized = False
    GameData(game_state)
    print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def next_move(data: GameData) -> str:
    next_move = "None"
    safes_around = data.safes_around()

    #体が極小の時: 優先度1
    if data.length() <= 2:
        if data.no_foods():
            next_move = random.choice(data.no_foods())
        elif data.safes_around():
            next_move = random.choice(data.safes_around())
        return next_move

    # 指定ルートがある場合(エサを探すとき): 優先度2
    if GameData.isDisignated:
        if GameData.disignated_route:
            next_move = GameData.disignated_route.popleft()
            if DEBUG:
                print(f"Disignated Move: {next_move}")
            return next_move
        else:
            GameData.isDisignated = False
            GameData.status = Status.loop

    # 体力に応じたエサ探索開始長さの設定
    starting_length = 0
    if 3 <= data.length() <= 4:
        starting_length = 12
    elif data.length() <= 12:
        starting_length = 10
    elif data.length() <= 15:
        starting_length = 13
    elif data.length() <= 20:
        starting_length = 16
    elif data.length() <= 25:
        starting_length = 18
    elif data.length() <= 30:
        starting_length = 22
    else:
        starting_length = 30

    # 体力が少ないときのエサ探索: 優先度3
    if data.health <= starting_length and not GameData.isDisignated:
        simulator = Simulation(game_data = data, max_depth = data.health)
        simulator.route_search(data = data)
        if simulator.result_tire1:
            GameData.disignated_route = max(simulator.result_tire1, key = len)
            print(f"Tire 1 route: {GameData.disignated_route}")
        elif simulator.result_tire2:
            GameData.disignated_route = max(simulator.result_tire2, key = len)
            print(f"Tire 2 route: {GameData.disignated_route}")
        elif simulator.result_tire3:
            GameData.disignated_route = max(simulator.result_tire3, key = len)
            print(f"Tire 3 route: {GameData.disignated_route}")

        if GameData.disignated_route:
            GameData.isDisignated = True
            GameData.status = Status.eat_food
            next_move = GameData.disignated_route.popleft()
            if DEBUG:
                print(f"Disignated Move: {next_move}")
            return next_move
        print("No route to food found!")
        
    # 進行可能方向がないor一つしかない場合の処理: 優先度4
    if not safes_around:
        if data.empty_around():
            next_move = random.choice(data.empty_around())
        else:
            if DEBUG:
                print("No safe move detected! move down!")
            next_move = "down"
        return next_move
    elif len(safes_around) == 1:
        if DEBUG:
            print("Only one safe move detected!")
        next_move = safes_around[0]
        return next_move

    # ループを探す動作: 優先度5
    if GameData.status == Status.loop:
        tire1 = []
        tire2 = []
        tire3 = []
        tire4 = []
        distance = {"up": data.tail()[Y] - data.head()[Y],
                    "down": data.head()[Y] - data.tail()[Y],
                    "right": data.tail()[X] - data.head()[X],
                    "left": data.head()[X] - data.tail()[X]}
        
        for move in safes_around:
            next_head = data.next_head_position(data.head(), move)
            new_body = data.bodies.copy()
            new_body.pop()
            new_body.appendleft(next_head)
            if Reachable(bodies = new_body, foods = data.foods, width = GameData.board_width, height = GameData.board_height).is_reachable_food_avoidance(next_head, data.tail()):
                if distance[move] > 0:
                    tire1.append(move)
                else:
                    tire2.append(move)
            elif Reachable(bodies = new_body, foods = data.foods, width = GameData.board_width, height = GameData.board_height).is_reachable(next_head, data.tail()):
                tire3.append(move)
                if distance[move] > 0:
                    tire3.append(move)
                else:
                    tire4.append(move)
        if tire1:
            next_move = max(tire1, key = lambda m: distance[m])
        elif tire2:
            next_move = random.choice(tire2)
        elif tire3:
            next_move = max(tire3, key = lambda m: distance[m]) 
        elif tire4:
            next_move = random.choice(tire4)
        else:
            if data.heading() in data.no_foods():
                next_move = data.heading()
            elif data.no_foods():
                next_move = random.choice(data.no_foods())
    
    if next_move == "None" and safes_around:
        next_move = random.choice(safes_around)
    return next_move

# 初期化やデバッグ表示など
def move(game_state: typing.Dict) -> typing.Dict:
    data = GameData(game_state)
    next_move_result = next_move(data)
    GameData.previous_foods = data.foods
    
    reachable_food_avoidance = []
    reachable = []
    if data.length() >= 3:
        bsf = Reachable(bodies = data.bodies, foods = data.foods, width = GameData.board_width, height = GameData.board_height)
        for move in data.safes_around():
            next_head = data.next_head_position(data.head(), move)
            new_body = data.bodies.copy()
            new_body.pop()
            new_body.appendleft(next_head)
            if bsf.is_reachable_food_avoidance(next_head, data.tail()):
                reachable_food_avoidance.append(move)
            if bsf.is_reachable(next_head, data.tail()):
                reachable.append(move)

    if DEBUG:
        print(f"safes around: {data.safes_around()}, no_foods around: {data.no_foods()}")
        print(f"foods: {data.foods}, bodies: {data.bodies}")
        print(f"reachable: {reachable} reachable_food_avoidance: {reachable_food_avoidance}")
        print(f"MOVE {game_state['turn']}: {next_move_result}")
        print(f"status: {GameData.status}")
        data.print_board()
    return {"move": next_move_result}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
