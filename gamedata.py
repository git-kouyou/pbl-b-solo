import typing
import random
import direction
from enum import Enum

class Status(Enum):
    find_food = 0
    loop = 1
    eat_food = 2
    

#データクラス
class GameData:
    board_height: int
    board_width: int
    wall: typing.List
    target_food: typing.Tuple[int, int]
    previous_foods = []
    target_pos: typing.Tuple[int, int]
    status: Status
    disignated_route: typing.List[str]
    isDisignated: bool
    initialized = False

    def __init__(self, game_state: typing.Dict = {}) -> None:
        if GameData.initialized == False:
            GameData.board_width = game_state["board"]["width"]
            GameData.board_height = game_state["board"]["height"]
            wall1 = [(x, -1) for x in range(-1, GameData.board_width + 1)]
            wall2 = [(x, GameData.board_height) for x in range(-1, GameData.board_width + 1)]
            wall3 = [(-1, y) for y in range(GameData.board_height)]
            wall4 = [(GameData.board_width, y) for y in range(GameData.board_height)]
            GameData.wall = wall1 + wall2 + wall3 + wall4
            GameData.status = Status.loop
            GameData.initialized = True
            GameData.disignated_route = []
            GameData.isDisignated = False
            print("GameData initialized")

        #体の座標(tuple)一覧
        self.bodies = [(body["x"], body["y"]) for body in game_state["you"]["body"]]
        #食べ物の座標(tuple)一覧
        self.foods = [(food["x"], food["y"]) for food in game_state["board"]["food"]]
        #頭の座標
        #self.head = (game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
        #尻尾の座標
        #self.tail = (game_state["you"]["body"][-1]["x"], game_state["you"]["body"][-1]["y"])
        #首の座標
        #if len(game_state["you"]["body"]) > 1:
        #    self.neck = (game_state["you"]["body"][1]["x"], game_state["you"]["body"][1]["y"])
        #長さ
        #self.length = len(game_state["you"]["body"])
        #方向
        #self.heading = direction.reverse(self.get_heading(self.neck, self.head)) if len(game_state["you"]["body"]) > 1 else "None"

    def head(self):
        return (self.bodies[0])
    
    def neck(self):
        return self.bodies[1] if len(self.bodies) > 1  else self.head()
    
    def heading(self):
        return self.get_heading(self.neck(), self.head())
    
    def tail(self):
        return self.bodies[-1]
    
    def length(self):
        return len(self.bodies)
    
    def unsafe_zones(self):
        result = []
        result = self.bodies + GameData.wall
        if self.tail() in result:
            result.remove(self.tail())
        return result
    
    def unsafes_around(self):
        return self.get_directions(self.head(), self.unsafe_zones())
    
    def foods_around(self):
        return self.get_directions(self.head(), self.foods)
    
    def foods_and_unsafes(self):
        return list(set(self.foods_around()) | set(self.unsafes_around()))
    
    def safes_around(self):
        return list(set(["up", "down", "left", "right"]) - set(self.unsafes_around()))
    
    def no_foods(self):
        return list(set(self.safes_around()) - set(self.foods_around()))

    def get_heading(self, from_pos, to_pos) -> str:
        direction = "None"
        if (from_pos[0] - 1, from_pos[1]) == to_pos:
            direction = "left"
        elif (from_pos[0] + 1, from_pos[1]) == to_pos:
            direction = "right"
        elif (from_pos[0], from_pos[1] + 1) == to_pos:
            direction = "up"
        elif (from_pos[0], from_pos[1] - 1) == to_pos:
            direction = "down"
        return direction
    
    def haeding(self):
        return self.get_heading(self.neck(), self.head())

    def set_target_food(self) -> None:
        self.target_food = random.choice(self.foods)
        print(f"ターゲットの食べ物を設定しました: {self.target_food}")

    def get_directions(self, from_pos, positions) -> typing.List[str]:
        result = []
        if (from_pos[0] + 1, from_pos[1]) in positions:
            result.append("right")
        if (from_pos[0], from_pos[1] + 1) in positions:
            result.append("up")
        if (from_pos[0] - 1, from_pos[1]) in positions:
            result.append("left")
        if (from_pos[0], from_pos[1] - 1) in positions:
            result.append("down")
        return result
    
    def get_directions_8(self, from_pos, positions) -> typing.List[str]:
        result = self.get_directions(from_pos, positions)
        if (from_pos[0] + 1, from_pos[1] + 1) in positions:
            result.append("upper_right")
        if (from_pos[0] - 1, from_pos[1] + 1) in positions:
            result.append("upper_left")
        if (from_pos[0] - 1, from_pos[1] - 1) in positions:
            result.append("downer_left")
        if (from_pos[0] + 1, from_pos[1] - 1) in positions:
            result.append("downer_right")
        return result
    
    def get_direction(self, from_pos, to_pos) -> str:
        direction = ""
        if (from_pos[0] - 1, from_pos[1]) == to_pos:
            direction = "left"
        elif (from_pos[0] + 1, from_pos[1]) == to_pos:
            direction = "right"
        elif (from_pos[0], from_pos[1] + 1) == to_pos:
            direction = "up"
        elif (from_pos[0], from_pos[1] - 1) == to_pos:
            direction = "down"
        return direction

    def set_target_food_random(self) -> None:
        GameData.target_food = random.choice(self.foods)

    def get_relative_directions(self, heading, from_pos, positions):
        result = []
        if heading == "right":
            if (from_pos[0] + 1, from_pos[1]) in positions:
                result.append("up")
            if (from_pos[0], from_pos[1] + 1) in positions:
                result.append("left")
            if (from_pos[0] - 1, from_pos[1]) in positions:
                result.append("down")
            if (from_pos[0], from_pos[1] - 1) in positions:
                result.append("right")
        elif heading == "up": 
            if (from_pos[0] + 1, from_pos[1]) in positions:
                result.append("right")
            if (from_pos[0], from_pos[1] + 1) in positions:
                result.append("up")
            if (from_pos[0] + 1, from_pos[1]) in positions:
                result.append("left")
            if (from_pos[0], from_pos[1]) in positions:
                result.append("down")
        elif heading == "left":
            if (from_pos[0] + 1, from_pos[1]) in positions:
                result.append("down")
            if (from_pos[0], from_pos[1] + 1) in positions:
                result.append("right")
            if (from_pos[0] - 1, from_pos[1]) in positions:
                result.append("up")
            if (from_pos[0], from_pos[1] - 1) in positions:
                result.append("left")
        elif heading == "down":
            if (from_pos[0] + 1, from_pos[1]) in positions:
                result.append("left")
            if (from_pos[0], from_pos[1] + 1) in positions:
                result.append("down")
            if (from_pos[0] - 1, from_pos[1]) in positions:
                result.append("right")
            if (from_pos[0], from_pos[1] - 1) in positions:
                result.append("up")
        return result