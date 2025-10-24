import typing
import random
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
    status: Status

    def __new__(cls, game_state: typing.Dict):
        GameData.board_width = game_state["board"]["width"]
        GameData.board_height = game_state["board"]["height"]
        wall1 = [(x, -1) for x in range(-1, GameData.board_width + 1)]
        wall2 = [(x, GameData.board_height) for x in range(-1, GameData.board_width + 1)]
        wall3 = [(-1, y) for y in range(GameData.board_height)]
        wall4 = [(GameData.board_width, y) for y in range(GameData.board_height)]
        GameData.wall = wall1 + wall2 + wall3 + wall4
        return super().__new__(cls)

    def __init__(self, game_state: typing.Dict) -> None:
        #体の座標(tuple)一覧
        self.bodies = [(body["x"], body["y"]) for body in game_state["you"]["body"]]
        #食べ物の座標(tuple)一覧
        self.foods = [(food["x"], food["y"]) for food in game_state["board"]["food"]]
        #頭の座標
        self.head = (game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
        #尻尾の座標
        self.tail = (game_state["you"]["body"][-1]["x"], game_state["you"]["body"][-1]["y"])
        #首の座標
        if len(game_state["you"]["body"]) > 1:
            self.neck = (game_state["you"]["body"][1]["x"], game_state["you"]["body"][1]["y"])

        #非安全地帯
        self.unsafe_zones = self.bodies + GameData.wall
        if self.tail in self.unsafe_zones:
            self.unsafe_zones.remove(self.tail)
        # 体と壁を避ける
        self.unsafes_around = self.get_directions(self.head, self.unsafe_zones)
        # 食べ物
        self.foods_around = self.get_directions(self.head, self.foods)
        # 食べ物と体と壁
        self.foods_and_unsafes = list(set(self.foods_around) | set(self.unsafes_around))
        # 安全地帯
        self.safes_around = list(set(["up", "down", "left", "right"]) - set(self.unsafes_around))
        # 食べ物なし
        self.no_foods = list(set(self.safes_around) - set(self.foods_around))

    def set_target_food(self) -> None:
        self.target_food = random.choice(self.foods)
        print(f"ターゲットの食べ物を設定しました: {self.target_food}")

    def get_directions(self, from_pos, positions) -> typing.List[str]:
        directions = []
        if (from_pos[0] - 1, from_pos[1]) in positions:
            directions.append("left")
        if (from_pos[0] + 1, from_pos[1]) in positions:
            directions.append("right")
        if (from_pos[0], from_pos[1] + 1) in positions:
            directions.append("up")
        if (from_pos[0], from_pos[1] - 1) in positions:
            directions.append("down")
        return directions
    
    def get_direction(self, target_pos, from_pos) -> str:
        direction = ""
        if (from_pos[0] - 1, from_pos[1]) == target_pos:
            direction = "left"
        elif (from_pos[0] + 1, from_pos[1]) == target_pos:
            direction = "right"
        elif (from_pos[0], from_pos[1] + 1) == target_pos:
            direction = "up"
        elif (from_pos[0], from_pos[1] - 1) == target_pos:
            direction = "down"
        return direction

    def set_target_food_random(self) -> None:
        GameData.target_food = random.choice(self.foods)