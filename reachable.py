from collections import deque
from gamedata import Type

X = 0
Y = 1

# 盤面表現: board[y][x]

# BSFによる到達可能判定
class Reachable:
    def __init__(self, foods, bodies, width, height) -> None:
        self.width = width
        self.height = height
        self.board = self.generate_board(foods, bodies)

    def generate_board(self, foods, bodies):
        # 盤面を初期化
        result = [[0] * (self.width) for _ in range(self.height)]
        # 体
        for i, body in enumerate(bodies):
            if body[X] - 1 < 0 and body[Y] - 1 < 0:
                continue
            result[body[Y] - 1][body[X] - 1] = len(bodies) - i
        # 食べ物
        for food in foods:
            result[food[Y] - 1][food[X] - 1] = Type.food.value
        return result

    def is_reachable(self, start: tuple[int, int], goal: tuple[int, int]) -> int:
        # gamedataの座標系からBSF用の座標系に変換
        start = (start[X] - 1, start[Y] - 1)
        goal = (goal[X] - 1, goal[Y] - 1)
        if start == goal:
            return True
        visited = [[False] * self.width for _ in range(self.height)]
        visited[start[Y]][start[X]] = True

        queue = deque([(start[X], start[Y], 0)])
        while queue:
            x, y, depth = queue.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                nd = depth + 1
                if 0 <= nx < self.width and 0 <= ny < self.height and not visited[ny][nx]:
                    if self.board[ny][nx] <= depth:
                        if (nx, ny) == goal:
                            return True
                        visited[ny][nx] = True
                        queue.append((nx, ny, nd))
        return False
    
    def is_reachable_food_avoidance(self, start: tuple[int, int], goal: tuple[int, int]) -> bool:
        start = (start[X] - 1, start[Y] - 1)
        goal = (goal[X] - 1, goal[Y] - 1)
        if start == goal:
            return True
        if self.board[start[Y]][start[X]] == Type.food.value or self.board[goal[Y]][goal[X]] == Type.food.value:
            return False
        visited = [[False] * self.height for _ in range(self.width)]
        visited[start[Y]][start[X]] = True

        queue = deque([(start[X], start[Y], 0)])
        while queue:
            x, y, depth = queue.popleft()
            nd = depth + 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.height and 0 <= ny < self.width and not visited[ny][nx]:
                    if 0 <= self.board[ny][nx] <= depth:
                        if (nx, ny) == goal:
                            return True
                        visited[ny][nx] = True
                        queue.append((nx, ny, nd))
        return False
    
    # デバッグ用盤面表示
    def print_board(self):
        for y in reversed(range(self.height)):
            row = ""
            for x in range(self.width):
                row += f"{self.board[y][x]}".rjust(2) + " "
            print(row)
        print()
    
# デバッグ用
if __name__ == "__main__":
    DEBUG = True
    foods = {(6, 1), (1, 5), (5, 2)}
    bodies = deque([(3, 1),(2, 1), (2, 2), (2, 3), (3, 3), (3, 4), (2, 4), (2, 5), (3, 5), (4, 5), (4, 4), (4, 3), (5, 3), (6, 3), (6, 4), (5, 4), (5, 5)])

    BSF = Reachable(foods = foods, bodies = bodies, width = 6, height = 6)
    BSF.print_board()

    start = (3, 1)
    goal = (6, 5)

    print(f"reachable food avoid:{BSF.is_reachable_food_avoidance(start, goal)}")
    print(f"reachable:{BSF.is_reachable(start, goal)}")