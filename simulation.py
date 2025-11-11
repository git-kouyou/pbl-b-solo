import typing
import random 
import copy
from gamedata import GameData
from gamedata import Type

class Simulation:
    def __init__(self, game_data: GameData, max_depth: int, rotation: typing.List[str] = []) -> None:
        self.game_data = game_data
        self.max_depth = max_depth
        self.rotation = rotation
        self.result = []

    def next_head_position(self, head: typing.Tuple[int, int], move: str) -> typing.Tuple[int, int]:
        next_head = (0, 0)
        if move == "right":
            next_head = (head[0] + 1, head[1])
        elif move == "up":
            next_head = (head[0], head[1] + 1)
        elif move == "left":
            next_head = (head[0] - 1, head[1])
        else:
            next_head = (head[0], head[1] - 1)

        return next_head
    
    def route_search_12(self, data: GameData, route: typing.List[str] = []):
        if data.head() in self.game_data.foods:
            data.bodies.append((0 , 0))  # 食べたら体が伸びる
            new_data = GameData(bodies = data.bodies, foods = data.foods)
            if len(new_data.safes_around()) > 0 and len(new_data.no_foods()) > 0:
                self.result.append(route)
            return
        if len(route) >= self.max_depth:
            return

        if len(data.safes_around()) == 0:
            return
        
        next = []
        distance = {"up": data.head()[1] - data.tail()[1],
                    "down": data.tail()[1] - data.head()[1],
                    "right": data.head()[0] - data.tail()[0],
                    "left": data.tail()[0] - data.head()[0]}
        
        if data.length() <= 8:
            next = data.safes_around()
        else:
            for move in data.safes_around():
                if distance[move] > 0 and move in data.safes_around():
                    next.append(move)
            if len(next) == 2:
                next = [min(next, key = lambda x: distance[x])]
            elif len(next) == 0:
                next = data.safes_around()
            
        for move in next:
            current_head = data.head()
            next_head = self.next_head_position(current_head, move)

            new_body = data.bodies.copy()
            new_body.pop(-1)
            new_body.insert(0, next_head)
            
            new_route = route + [move]

            new_data = GameData(bodies = new_body, foods = data.foods)
            self.route_search_12(data=new_data, route=new_route)
