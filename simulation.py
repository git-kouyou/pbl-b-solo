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
            new_body = data.bodies.copy()
            new_body.append(new_body[-1])  # 食べたら体が伸びる
            new_data = GameData(bodies = new_body, foods = data.foods)
            if len(new_data.safes_around()) > 0 and len(new_data.no_foods()) > 0:
                self.result.append(route)
            return
        
        if len(route) >= self.max_depth:
            return

        if len(data.safes_around()) == 0:
            return
        
        for move in data.safes_around():
            current_head = data.head()
            next_head = self.next_head_position(current_head, move)

            new_body = data.bodies.copy()
            new_body.pop(-1)
            new_body.insert(0, next_head)
            
            new_route = route + [move]

            new_data = GameData(bodies = new_body, foods = data.foods)
            self.route_search_12(data=new_data, route=new_route)

    def route_search_24(self, data: GameData, route: typing.List[str] = []):
        if data.board[data.head()[0]][data.head()[1]] == Type.food.value:
            new_body = data.bodies.copy()
            new_body.append(new_body[-1])  # 食べたら体が伸びる
            new_data = GameData(bodies = new_body, foods = data.foods)
            if len(new_data.no_foods()) > 0:
                self.result.append(route)
            return
        if len(route) >= self.max_depth:
            return
        
        predicate = {"up": (1, GameData.board_height), "down": (1, 1), "left": (0, 1), "right": (0, GameData.board_width)}
        if data.head()[predicate[GameData.rotate_direction[1]][0]] == predicate[GameData.rotate_direction[1]][1]:
            GameData.rotate_direction = [GameData.rotate_direction[1], data.reverse(GameData.rotate_direction[0])]
            print(f"Rotate direction changed to: {GameData.rotate_direction}")
        
        candidate = [GameData.rotate_direction[0], GameData.rotate_direction[1], data.reverse(GameData.rotate_direction[1])]
        for move in candidate:
            if move in data.safes_around():
                current_head = data.head()
                next_head = self.next_head_position(current_head, move)

                new_body = data.bodies.copy()
                new_body.pop(-1)
                new_body.insert(0, next_head)
                
                new_route = route + [move]

                new_data = GameData(bodies = new_body, foods = data.foods)
                self.route_search_24(data=new_data, route=new_route)
