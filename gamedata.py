import typing
import random
from enum import Enum

class Status(Enum):
    find_food = 0
    loop = 1
    eat_food = 2

class Type(Enum):
    safe = 0
    food = 1
    body = 2
    wall = 100

#データクラス
class GameData:
    board_height: int
    board_width: int
    wall: typing.List
    target_food: typing.Tuple[int, int]
    previous_foods = []
    target_pos: typing.Tuple[int, int]
    status: Status = Status.loop
    disignated_route: typing.List[str] = []
    isDisignated: bool = False
    rotate_direction: typing.List[str] = []
    initialized = False

    def __init__(self, game_state: typing.Dict = {}, bodies = [], foods = []):
        if game_state == {} and bodies == []:
            print("cannot initialize GameData!")
            exit(1)

        if GameData.initialized == False:
            if game_state == {}:
                print("information for initialization is insufficient!")
                exit(1)
            #幅と高さの設定
            GameData.board_width = game_state["board"]["width"]
            GameData.board_height = game_state["board"]["height"]

            #壁の座標(tuple)一覧
            wall1 = [(x, 0) for x in range(GameData.board_width + 1)]
            wall2 = [(x, GameData.board_height + 1) for x in range(GameData.board_width + 1)]
            wall3 = [(0, y) for y in range(1, GameData.board_height + 1)]
            wall4 = [(GameData.board_width + 1, y) for y in range(1, GameData.board_height + 1)]
            GameData.wall = wall1 + wall2 + wall3 + wall4

            #初期化済み
            GameData.initialized = True
            print("GameData initialized")

        ##################
        self.game_state = game_state
        #体の座標(tuple)一覧
        self.bodies = [(body["x"] + 1, body["y"] + 1) for body in game_state["you"] ["body"]] if bodies == [] else bodies
        #食べ物の座標(tuple)一覧
        self.foods = [(food["x"] + 1, food["y"] + 1) for food in game_state["board"]["food"]] if foods == [] else foods
        #盤面のデータ
        self.board = self.generate_board()
    
    def generate_board(self):
        result: typing.List[typing.List[int]] = [[0] * (GameData.board_width + 2) for _ in range(GameData.board_height + 2)]
        for i in range(len(self.bodies)):
            result[self.bodies[i][0]][self.bodies[i][1]] = len(self.bodies) - i + Type.body.value - 2
        for food in self.foods:
            result[food[0]][food[1]] = 1
        for i in range(GameData.board_width + 2):
            result[i][0] = Type.wall.value
            result[i][GameData.board_height + 1] = Type.wall.value
        for j in range(GameData.board_height + 2):
            result[0][j] = Type.wall.value
            result[GameData.board_width + 1][j] = Type.wall.value
        return result

    def head(self):
        return self.bodies[0]
    
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
        result = []
        # if (self.head()[0] + 1, self.head()[1]) in self.unsafe_zones():
        #     result.append("right")
        # if (self.head()[0], self.head()[1] + 1) in self.unsafe_zones():
        #     result.append("up")
        # if (self.head()[0] - 1, self.head()[1]) in self.unsafe_zones():
        #     result.append("left")
        # if (self.head()[0], self.head()[1] - 1) in self.unsafe_zones():
        #     result.append("down")
        if self.board[self.head()[0] + 1][self.head()[1]] >= Type.body.value:
            result.append("right")
        if self.board[self.head()[0]][self.head()[1] + 1] >= Type.body.value:
            result.append("up")
        if self.board[self.head()[0] - 1][self.head()[1]] >= Type.body.value:
            result.append("left")
        if self.board[self.head()[0]][self.head()[1] - 1] >= Type.body.value:
            result.append("down")
        return result
    
    def foods_around(self):
        result = []
        if self.board[self.head()[0] + 1][self.head()[1]] == Type.food.value:
            result.append("right")
        if self.board[self.head()[0]][self.head()[1] + 1] == Type.food.value:
            result.append("up")
        if self.board[self.head()[0] - 1][self.head()[1]] == Type.food.value:
            result.append("left")
        if self.board[self.head()[0]][self.head()[1] - 1] == Type.food.value:
            result.append("down")
        return result
    
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

    # def get_directions(self, from_pos, to_pos) -> typing.List[str]:
    #     result = []
    #     if self.board[from_pos[0] + 1][from_pos[1]] in to_pos:
    #         result.append("right")
    #     if self.board[from_pos[0]][from_pos[1] + 1] in to_pos:
    #         result.append("up")
    #     if self.board[from_pos[0] - 1][from_pos[1]] in to_pos:
    #         result.append("left")
    #     if self.board[from_pos[0]][from_pos[1] - 1] in to_pos:
    #         result.append("down")
    #     return result
    
    # def get_directions_8(self, from_pos, positions) -> typing.List[str]:
    #     result = self.get_directions(from_pos, positions)
    #     if (from_pos[0] + 1, from_pos[1] + 1) in positions:
    #         result.append("upper_right")
    #     if (from_pos[0] - 1, from_pos[1] + 1) in positions:
    #         result.append("upper_left")
    #     if (from_pos[0] - 1, from_pos[1] - 1) in positions:
    #         result.append("downer_left")
    #     if (from_pos[0] + 1, from_pos[1] - 1) in positions:
    #         result.append("downer_right")
    #     return result
    
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
    
    def move_direction_24(self):
        if GameData.rotate_direction == []:
            GameData.rotate_direction = ["up", "right"]
        
        predicate = {"up": (1, GameData.board_height), "down": (1, 1), "left": (0, 1), "right": (0, GameData.board_width)}
        if self.head()[predicate[GameData.rotate_direction[0]][0]] == predicate[GameData.rotate_direction[0]][1]:
            GameData.rotate_direction = [GameData.rotate_direction[1], self.reverse(GameData.rotate_direction[0])]

        if GameData.rotate_direction[0] in self.dangerous():
            return GameData.rotate_direction[0]
        elif GameData.rotate_direction[1] in self.dangerous():
            return GameData.rotate_direction[1]
        else:
            if len(self.dangerous()) > 0:
                return random.choice(self.dangerous())
            else:
                return "None"
    
    def reverse(self, direction: str) -> str:
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        elif direction == "right":
            return "left"
        else:
            return "None"
        
    def dangerous(self):
        result = []
        if self.board[self.head()[0] + 1][self.head()[1] + 1] >= Type.body.value and self.board[self.head()[0] + 1][self.head()[1] - 1] >= Type.body.value:
            result.append("right")
        if self.board[self.head()[0] - 1][self.head()[1] + 1] >= Type.body.value and self.board[self.head()[0] + 1][self.head()[1] + 1] >= Type.body.value:
            result.append("up")
        if self.board[self.head()[0] - 1][self.head()[1] + 1] >= Type.body.value and self.board[self.head()[0] - 1][self.head()[1] - 1] >= Type.body.value:
            result.append("left")
        if self.board[self.head()[0] + 1][self.head()[1] - 1] >= Type.body.value and self.board[self.head()[0] - 1][self.head()[1] - 1] >= Type.body.value:
            result.append("down")
        return result