import typing
from collections import deque
from gamedata import GameData
from reachable import Reachable

Y = 1
X = 0

class Simulation:
    def __init__(self, game_data: GameData, max_depth: int) -> None:
        #シミュレーション用データ
        self.game_data = game_data
        #最大の経路
        self.max_depth = max_depth
        #経路探索結果
        self.result_tire1 = []
        self.result_tire2 = []
        self.result_tire3 = []
        #長さが3〜4のときの探索済み経路保存用
        self.dumped_route_34: typing.Dict[typing.Tuple[typing.Tuple[int, int], str], typing.Set[int]] = {}

    #新版
    def route_search_new(self, data: GameData, route: deque = deque()):
        #餌を食べたら経路を保存して終了
        if data.head() in data.foods:
            tail = data.tail()
            data.bodies.append((0, 0))
            new_foods = data.foods.copy()
            new_foods.remove(data.head())
            if Reachable(bodies = data.bodies, foods = new_foods, width = GameData.board_width, height = GameData.board_height).is_reachable_tail_food_avoidance(data.head(), tail):
                self.result_tire1.append(route)
            elif Reachable(bodies = data.bodies, foods = new_foods, width = GameData.board_width, height = GameData.board_height).is_reachable_tail(data.head(), tail):
                self.result_tire2.append(route)    
            return

        #最大深度に達したら終了
        if len(route) >= self.max_depth:
            return
        #進行可能方向がない場合終了
        if not data.safes_around():
            return

        next = deque()
        #長さが3〜4のときは全探索するが，頭の位置と首の向きが同じで体の長さも同じ場合は探索済みとして終了
        if data.length() <= 4:
            current_head = data.head()
            for move in data.safes_around():
                next_head = data.next_head_position(current_head, move)
                if (next_head, data.neck_direction()) in self.dumped_route_34.keys():
                    if data.length() in self.dumped_route_34[(next_head, data.neck_direction())]:
                        continue
                    self.dumped_route_34[(next_head, data.neck_direction())].add(data.length())
                else:
                    self.dumped_route_34[(next_head, data.neck_direction())] = set([data.length()])
                next.append(move)
        else:
            next = deque(data.safes_around())
            
        for move in next:
            current_head = data.head()
            next_head = data.next_head_position(current_head, move)

            new_body = data.bodies.copy()
            new_body.pop()
            new_body.appendleft(next_head)
            
            new_route = route.copy()
            new_route.append(move)

            if Reachable(bodies = new_body, foods = data.foods, width = self.game_data.board_width, height = self.game_data.board_height).is_reachable_tail(next_head, data.tail()):
                new_data = GameData(bodies = new_body, foods = data.foods)
                self.route_search_new(data = new_data, route = new_route)