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
    previous_foods = []
    target_pos: typing.Tuple[int, int] = tuple()
    status: Status = Status.loop
    disignated_route: typing.List[str] = []
    isDisignated: bool = False
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

            #初期化済み
            GameData.initialized = True
            print("GameData initialized")

        #体の座標(tuple)一覧
        self.bodies = []
        if bodies == []:
            seen = set()
            for body in game_state["you"]["body"]:
                pos = (body["x"] + 1, body["y"] + 1)
                if pos not in seen:
                    seen.add(pos)
                    self.bodies.append(pos)
        else:
            self.bodies = bodies
        #食べ物の座標(tuple)一覧
        self.foods = [(food["x"] + 1, food["y"] + 1) for food in game_state["board"]["food"]] if foods == [] else foods
        #盤面のデータ
        self.board = self.generate_board()
        #残り体力
        self.health = game_state["you"]["health"] if "you" in game_state else 100
    
    def generate_board(self):
        result = [[Type.safe.value] * (GameData.board_width + 2) for _ in range(GameData.board_height + 2)]
        #体
        if self.length() < 3 or self.ate_food():
            for i in range(self.length()):
                result[self.bodies[i][0]][self.bodies[i][1]] = self.length() - i + Type.body.value - 1  # 頭に近いほど値が大きい
        else:
            for i in range(self.length() - 1):
                result[self.bodies[i][0]][self.bodies[i][1]] = self.length() - i + Type.body.value - 2  # 頭に近いほど値が大きい
        #食べ物
        for food in self.foods:
            result[food[0]][food[1]] = Type.food.value
        #壁(縦)
        for i in range(GameData.board_width + 2):
            result[i][0] = Type.wall.value
            result[i][GameData.board_height + 1] = Type.wall.value
        #壁(横)
        for j in range(GameData.board_height + 2):
            result[0][j] = Type.wall.value
            result[GameData.board_width + 1][j] = Type.wall.value
        return result

    def print_board(self):
        for x in range(GameData.board_height + 2):
            row = ""
            for y in range(GameData.board_width + 2):
                if self.board[y][GameData.board_height + 1 - x] != Type.wall.value:
                    row += f"{self.board[y][GameData.board_height + 1 - x]}".zfill(2) + " "
                else:
                    row += "## "
            print(row)

    def ate_food(self):
        return self.previous_foods != self.foods

    def head(self):
        return self.bodies[0]
    
    def neck(self):
        return self.bodies[1] if len(self.bodies) > 1  else self.head()
    
    def tail(self):
        return self.bodies[-1]
    
    def length(self):
        return len(self.bodies)
    
    def empty_around(self):
        result = []
        if self.board[self.head()[0] + 1][self.head()[1]] == Type.safe.value:
            result.append("right")
        if self.board[self.head()[0]][self.head()[1] + 1] == Type.safe.value:
            result.append("up")
        if self.board[self.head()[0] - 1][self.head()[1]] == Type.safe.value:
            result.append("left")
        if self.board[self.head()[0]][self.head()[1] - 1] == Type.safe.value:
            result.append("down")
        return result
    
    def unsafes_around(self):
        result = []
        if self.board[self.head()[0] + 1][self.head()[1]] >= Type.body.value:
            result.append("right")
        if self.board[self.head()[0]][self.head()[1] + 1] >= Type.body.value:
            result.append("up")
        if self.board[self.head()[0] - 1][self.head()[1]] >= Type.body.value:
            result.append("left")
        if self.board[self.head()[0]][self.head()[1] - 1] >= Type.body.value:
            result.append("down")
        if "right" not in result and self.board[self.head()[0] + 1][self.head()[1] + 1] >= Type.body.value + 1 and self.board[self.head()[0] + 2][self.head()[1]] >= Type.body.value + 1 and self.board[self.head()[0] + 1][self.head()[1] - 1] >= Type.body.value + 1:
            result.append("right")
        if "up" not in result and self.board[self.head()[0] + 1][self.head()[1] + 1] >= Type.body.value + 1 and self.board[self.head()[0]][self.head()[1] + 2] >= Type.body.value + 1 and self.board[self.head()[0] - 1][self.head()[1] + 1] >= Type.body.value + 1:
            result.append("up")
        if "left" not in result and self.board[self.head()[0] - 1][self.head()[1] + 1] >= Type.body.value + 1 and self.board[self.head()[0] - 2][self.head()[1]] >= Type.body.value + 1 and self.board[self.head()[0] - 1][self.head()[1] - 1] >= Type.body.value + 1:
            result.append("left")
        if "down" not in result and self.board[self.head()[0] + 1][self.head()[1] - 1] >= Type.body.value + 1 and self.board[self.head()[0]][self.head()[1] - 2] >= Type.body.value + 1 and self.board[self.head()[0] - 1][self.head()[1] - 1] >= Type.body.value + 1:
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
    
    def safes_around(self):
        result = [] 
        if self.board[self.head()[0] + 1][self.head()[1]] <= Type.food.value:
            result.append("right")
        if self.board[self.head()[0]][self.head()[1] + 1] <= Type.food.value:
            result.append("up")
        if self.board[self.head()[0] - 1][self.head()[1]] <= Type.food.value:
            result.append("left")   
        if self.board[self.head()[0]][self.head()[1] - 1] <= Type.food.value:
            result.append("down")
        if "right" in result:
            if self.board[self.head()[0] + 1][self.head()[1] + 1] >= Type.body.value + 1 and self.board[self.head()[0] + 2][self.head()[1]] >= Type.body.value + 1 and self.board[self.head()[0] + 1][self.head()[1] - 1] >= Type.body.value + 1:
                result.remove("right")
        if "up" in result:
            if self.board[self.head()[0] + 1][self.head()[1] + 1] >= Type.body.value + 1 and self.board[self.head()[0]][self.head()[1] + 2] >= Type.body.value + 1 and self.board[self.head()[0] - 1][self.head()[1] + 1] >= Type.body.value + 1:
                result.remove("up")
        if "left" in result:
            if self.board[self.head()[0] - 1][self.head()[1] + 1] >= Type.body.value + 1 and self.board[self.head()[0] - 2][self.head()[1]] >= Type.body.value + 1 and self.board[self.head()[0] - 1][self.head()[1] - 1] >= Type.body.value + 1:
                result.remove("left")
        if "down" in result:
            if self.board[self.head()[0] + 1][self.head()[1] - 1] >= Type.body.value + 1 and self.board[self.head()[0]][self.head()[1] - 2] >= Type.body.value + 1 and self.board[self.head()[0] - 1][self.head()[1] - 1] >= Type.body.value + 1:
                result.remove("down")
        return result
    
    def no_foods(self):
        return list(set(self.safes_around()) - set(self.foods_around()))
    
    # def get_heading(self, from_pos, to_pos) -> str:
    #     direction = "None"
    #     if (from_pos[0] - 1, from_pos[1]) == to_pos:
    #         direction = "left"
    #     elif (from_pos[0] + 1, from_pos[1]) == to_pos:
    #         direction = "right"
    #     elif (from_pos[0], from_pos[1] + 1) == to_pos:
    #         direction = "up"
    #     elif (from_pos[0], from_pos[1] - 1) == to_pos:
    #         direction = "down"
    #     return direction
    
    def heading(self):
        if self.head()[0] < self.neck()[0]:
            return "left"
        elif self.head()[0] > self.neck()[0]:
            return "right"
        elif self.head()[1] < self.neck()[1]:
            return "down"
        elif self.head()[1] > self.neck()[1]:
            return "up"
        
    def neck_direction(self):
        if self.neck()[0] < self.head()[0]:
            return "left"
        elif self.neck()[0] > self.head()[0]:
            return "right"
        elif self.neck()[1] < self.head()[1]:
            return "down"
        else:
            return "up"
        
    # def get_direction(self, from_pos, to_pos) -> str:
    #     direction = ""
    #     if (from_pos[0] - 1, from_pos[1]) == to_pos:
    #         direction = "left"
    #     elif (from_pos[0] + 1, from_pos[1]) == to_pos:
    #         direction = "right"
    #     elif (from_pos[0], from_pos[1] + 1) == to_pos:
    #         direction = "up"
    #     elif (from_pos[0], from_pos[1] - 1) == to_pos:
    #         direction = "down"
    #     return direction