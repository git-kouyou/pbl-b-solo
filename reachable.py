import typing
import copy
from gamedata import Type
from collections import deque

class Reachable:
    def __init__(self, foods, bodies, width, height) -> None:
        self.width = width
        self.height = height
        self.board = self.generate_board(foods, bodies)

    def generate_board(self, foods, bodies):
        # 盤面を初期化 (board[y][x])、入力は (x,y) 形式を想定
        result = [[0] * (self.width) for _ in range(self.height)]
        # 体 (頭に近いほど値が大きい)
        for i in range(len(bodies)):
            x, y = bodies[i][0] - 1, bodies[i][1] - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                result[y][x] = len(bodies) - i
        # 食べ物
        for food in foods:
            fx, fy = food[0] - 1, food[1] - 1
            if 0 <= fx < self.width and 0 <= fy < self.height:
                result[fy][fx] = -1
        return result

    def is_reachable_tail(self, start: typing.Tuple[int, int]) -> bool:
        """
        start (x,y) から尾 (board 値 == 1) に到達可能かを判定します。
        この関数は食べ物マス(-1)を通行可能として扱います。
        """
        sx, sy = start[0] - 1, start[1] - 1
        if not (0 <= sx < self.width and 0 <= sy < self.height):
            return False

        visited = [[False] * self.width for _ in range(self.height)]
        visited[sy][sx] = True
        queue = deque([(sx, sy, 0)])  # (x, y, dist)

        while queue:
            x, y, dist = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                nd = dist + 1
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if visited[ny][nx]:
                        continue
                    cell = self.board[ny][nx]
                    # food(-1) は通行可能
                    # マスが nd ターン目までに空く (cell <= nd) か、初めから空 (cell == 0) なら進める
                    if cell == -1 or (0 <= cell <= nd):
                        # tail は値が 1（generate_board の定義）
                        if cell == 1:
                            return True
                        visited[ny][nx] = True
                        queue.append((nx, ny, nd))
        return False
    
    def is_reachable_tail_food_avoidance(self, start: typing.Tuple[int, int]) -> bool:
        """
        start (x,y) から尾 (board 値 == 1) に到達可能かを判定します。
        この関数は食べ物マス(-1) を通行禁止とします（食べ物を避ける）。
        """
        sx, sy = start[0] - 1, start[1] - 1
        if not (0 <= sx < self.width and 0 <= sy < self.height):
            return False

        visited = [[False] * self.width for _ in range(self.height)]
        visited[sy][sx] = True
        queue = deque([(sx, sy, 0)])  # (x, y, dist)

        while queue:
            x, y, dist = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                nd = dist + 1
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if visited[ny][nx]:
                        continue
                    cell = self.board[ny][nx]
                    # 食べ物マスは避ける
                    if cell == -1:
                        continue
                    if 0 <= cell <= nd:
                        if cell == 1:
                            return True
                        visited[ny][nx] = True
                        queue.append((nx, ny, nd))
        return False