import typing
from collections import deque
from enum import Enum

X = 0
Y = 1

class Status(Enum):
    loop = 0
    eat_food = 1

# 盤面上の各マスの種類
class Type(Enum):
    safe = 0
    food = -1
    body = 1
    wall = 100

# データクラス
class GameData:
    board_height: int
    board_width: int
    previous_foods:typing.Set[typing.Tuple[int, int]]
    status: Status = Status.loop
    disignated_route: deque
    isDisignated: bool
    initialized = False

    def __init__(self, game_state: typing.Dict = {}, bodies = set(), foods = []):
        if game_state == {} and bodies == []:
            print("cannot initialize GameData!")
            exit(1)

        # 初生成時にクラス変数を初期化
        if not GameData.initialized:
            if game_state == {}:
                print("information for initialization is insufficient!")
                exit(1)
            #幅と高さの設定
            GameData.board_width = game_state["board"]["width"]
            GameData.board_height = game_state["board"]["height"]
            GameData.previous_foods = set()
            GameData.status = Status.loop
            GameData.disignated_route = deque()
            GameData.isDisignated = False
            #初期化済み
            GameData.initialized = True
            print("GameData initialized")

        # 体の座標(tuple)一覧
        self.bodies = deque()
        if not bodies:
            seen = set()
            for body in game_state["you"]["body"]:
                pos = (body["x"] + 1, body["y"] + 1)
                if pos not in seen:
                    seen.add(pos)
                    self.bodies.append(pos)
        else:
            self.bodies = bodies
        # 食べ物の座標(tuple)一覧
        self.foods = set([(food["x"] + 1, food["y"] + 1) for food in game_state["board"]["food"]]) if not foods else foods
        # 盤面のデータ
        self.generate_board()
        # 残り体力
        self.health = game_state["you"]["health"] if "you" in game_state else 100
    
    # 盤面データの生成
    def generate_board(self):
        # 盤面を初期化
        self.board = [[Type.safe.value] * (GameData.board_width + 2) for _ in range(GameData.board_height + 2)]
        # 壁(縦)
        for i in range(GameData.board_width + 2):
            self.board[i][0] = Type.wall.value
            self.board[i][GameData.board_height + 1] = Type.wall.value
        # 壁(横)
        for j in range(GameData.board_height + 2):
            self.board[0][j] = Type.wall.value
            self.board[GameData.board_width + 1][j] = Type.wall.value
        # 体
        if self.length() < 3 or self.ate_food():
            for i in range(self.length()):
                self.board[self.bodies[i][Y]][self.bodies[i][X]] = self.length() - i + Type.body.value - 1  # 頭に近いほど値が大きい
        else:
            for i in range(self.length() - 1):
                self.board[self.bodies[i][Y]][self.bodies[i][X]] = self.length() - i + Type.body.value - 2  # 頭に近いほど値が大きい
        # 食べ物
        for food in self.foods:
            self.board[food[Y]][food[X]] = Type.food.value

    # デバッグ用盤面表示
    def print_board(self):
        for y in reversed(range(GameData.board_height + 2)):
            row = ""
            for x in range(GameData.board_width + 2):
                if self.board[y][GameData.board_width + 1 - x] != Type.wall.value:
                    row += f"{self.board[y][GameData.board_width + 1 - x]}".zfill(2) + " "
                else:
                    row += "## "
            print(row)

    # 餌を食べた直後ならばTrueを返す
    def ate_food(self):
        return self.previous_foods != self.foods

    # 頭の座標
    def head(self):
        return self.bodies[0]
    
    # 首の座標
    def neck(self):
        return self.bodies[1] if len(self.bodies) > 1  else self.head()
    
    # 尾の座標
    def tail(self):
        return self.bodies[-1]
    
    # 体の長さ
    def length(self):
        return len(self.bodies)
    
    # 周りの進行可能方向のリスト
    def empty_around(self):
        result = []
        if self.board[self.head()[Y]][self.head()[X] + 1] <= Type.food.value:
            result.append("right")
        if self.board[self.head()[Y] + 1][self.head()[X]] <= Type.food.value:
            result.append("up")
        if self.board[self.head()[Y]][self.head()[X] - 1] <= Type.food.value:
            result.append("left")
        if self.board[self.head()[Y] - 1][self.head()[X]] <= Type.food.value:
            result.append("down")
        return result
    
    # 進行不可能方向(潜在的な詰み含む)のリスト
    def unsafes_around(self):
        result = []
        if self.board[self.head()[Y]][self.head()[X] + 1] >= Type.body.value + 1:
            result.append("right")
        if self.board[self.head()[Y] + 1][self.head()[X]] >= Type.body.value + 1:
            result.append("up")
        if self.board[self.head()[Y]][self.head()[X] - 1] >= Type.body.value + 1:
            result.append("left")
        if self.board[self.head()[Y] - 1][self.head()[X]] >= Type.body.value + 1:
            result.append("down")
        # if "right" not in result and self.board[self.head()[Y] + 1][self.head()[X] + 1] >= Type.body.value + 1 and self.board[self.head()[Y]][self.head()[X] + 2] >= Type.body.value + 1 and self.board[self.head()[Y] - 1][self.head()[X] + 1] >= Type.body.value + 1:
        #     result.append("right")
        # if "up" not in result and self.board[self.head()[Y] + 1][self.head()[X] + 1] >= Type.body.value + 1 and self.board[self.head()[Y] + 2][self.head()[X]] >= Type.body.value + 1 and self.board[self.head()[Y] + 1][self.head()[X] - 1] >= Type.body.value + 1:
        #     result.append("up")
        # if "left" not in result and self.board[self.head()[Y] + 1][self.head()[X] - 1] >= Type.body.value + 1 and self.board[self.head()[Y]][self.head()[X] - 2] >= Type.body.value + 1 and self.board[self.head()[Y] - 1][self.head()[X] - 1] >= Type.body.value + 1:
        #     result.append("left")
        # if "down" not in result and self.board[self.head()[Y] + 1][self.head()[X] - 1] >= Type.body.value + 1 and self.board[self.head()[Y]][self.head()[X] - 2] >= Type.body.value + 1 and self.board[self.head()[Y] - 1][self.head()[X] - 1] >= Type.body.value + 1:
        #     result.append("down")
        return result
    
    # 周りの餌のある方向のリスト
    def foods_around(self):
        result = []
        if self.board[self.head()[Y]][self.head()[X] + 1] == Type.food.value:
            result.append("right")
        if self.board[self.head()[Y] + 1][self.head()[X]] == Type.food.value:
            result.append("up")
        if self.board[self.head()[Y]][self.head()[X] - 1] == Type.food.value:
            result.append("left")
        if self.board[self.head()[Y] - 1][self.head()[X]] == Type.food.value:
            result.append("down")
        return result
    
    # 周りの安全な方向のリスト
    def safes_around(self):
        result = [] 
        if self.board[self.head()[Y]][self.head()[X] + 1] <= Type.safe.value:
            result.append("right")
        if self.board[self.head()[Y] + 1][self.head()[X]] <= Type.safe.value:
            result.append("up")
        if self.board[self.head()[Y]][self.head()[X] - 1] <= Type.safe.value:
            result.append("left")   
        if self.board[self.head()[Y] - 1][self.head()[X]] <= Type.safe.value:
            result.append("down")
        # if "right" in result:
        #     if self.board[self.head()[Y] + 1][self.head()[X] + 1] >= Type.body.value + 1 and self.board[self.head()[Y]][self.head()[X] + 2] >= Type.body.value + 1 and self.board[self.head()[Y] - 1][self.head()[X] + 1] >= Type.body.value + 1:
        #         result.remove("right")
        # if "up" in result:
        #     if self.board[self.head()[Y] + 1][self.head()[X] + 1] >= Type.body.value + 1 and self.board[self.head()[Y] + 2][self.head()[X]] >= Type.body.value + 1 and self.board[self.head()[Y] + 1][self.head()[X] - 1] >= Type.body.value + 1:
        #         result.remove("up")
        # if "left" in result:
        #     if self.board[self.head()[Y] + 1][self.head()[X] - 1] >= Type.body.value + 1 and self.board[self.head()[Y]][self.head()[X] - 2] >= Type.body.value + 1 and self.board[self.head()[Y] - 1][self.head()[X] - 1] >= Type.body.value + 1:
        #         result.remove("left")
        # if "down" in result:
        #     if self.board[self.head()[Y] + 1][self.head()[X] - 1] >= Type.body.value + 1 and self.board[self.head()[Y]][self.head()[X] - 2] >= Type.body.value + 1 and self.board[self.head()[Y] - 1][self.head()[X] - 1] >= Type.body.value + 1:
        #         result.remove("down")
        return result
    
    # 餌のない安全な方向のリスト
    def no_foods(self):
        return list(set(self.safes_around()) - set(self.foods_around()))
    
    # 現在の進行方向
    def heading(self):
        if self.head()[X] < self.neck()[X]:
            return "left"
        elif self.head()[X] > self.neck()[X]:
            return "right"
        elif self.head()[Y] < self.neck()[Y]:
            return "down"
        else:
            return "up"
    
    # 向きの反転
    def reverse_direction(self, direction: str) -> str:
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        else:
            return "left"
        
    #進む方向によって次の頭の位置を返す
    def next_head_position(self, head: typing.Tuple[int, int], move: str) -> typing.Tuple[int, int]:
        if move == "right":
            return (head[X] + 1, head[Y])
        elif move == "up":
            return (head[X], head[Y] + 1)
        elif move == "left":
            return (head[X] - 1, head[Y])
        else:
            return (head[X], head[Y] - 1)