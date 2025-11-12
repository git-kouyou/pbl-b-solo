import typing
from collections import deque

# BSF用のクラス
class Reachable:
    def __init__(self, foods, bodies, width, height) -> None:
        self.width = width
        self.height = height
        self.board = self.generate_board(foods, bodies)

    def generate_board(self, foods, bodies):
        # 盤面を初期化 (board[y][x])
        result = [[0] * (self.width) for _ in range(self.height)]
        # 体 (頭に近いほど値が大きい).補正のために -1
        for i in range(len(bodies)):
            x, y = bodies[i][0] - 1, bodies[i][1] - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                result[y][x] = len(bodies) - i
        # 食べ物
        for food in foods:
            x, y = food[0] - 1, food[1] - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                result[y][x] = -1
        return result

    #しっぽに到達可能か判定（エサを通る可能性あり）
    def is_reachable_tail(self, start: typing.Tuple[int, int]) -> bool:
        start_x, start_y = start[0] - 1, start[1] - 1
        if not (0 <= start_x < self.width and 0 <= start_y < self.height):
            return False

        visited = [[False] * self.width for _ in range(self.height)]
        visited[start_y][start_x] = True
        queue = deque([(start_x, start_y, 0)])

        while queue:
            x, y, dist = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                nd = dist + 1
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if visited[ny][nx]:
                        continue
                    cell = self.board[ny][nx]
                    if cell == -1 or (0 <= cell <= nd):
                        if cell == 1:
                            return True
                        visited[ny][nx] = True
                        queue.append((nx, ny, nd))
        return False
    
    #しっぽに到達可能か判定（エサを通らない）
    def is_reachable_tail_food_avoidance(self, start: typing.Tuple[int, int]) -> bool:
        start_x, start_y = start[0] - 1, start[1] - 1
        if not (0 <= start_x < self.width and 0 <= start_y < self.height):
            return False

        visited = [[False] * self.width for _ in range(self.height)]
        visited[start_y][start_x] = True
        queue = deque([(start_x, start_y, 0)])

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